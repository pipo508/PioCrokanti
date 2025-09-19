// server.js - VERSIÓN OPTIMIZADA
require('dotenv').config();

const express = require('express');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs').promises;
const path = require('path');

async function init() {
  // ------------------------
  // Inicializar fetch con fallback
  // ------------------------
  let fetchFn = null;

  if (typeof globalThis.fetch === 'function') {
    fetchFn = globalThis.fetch;
  } else {
    try {
      const undici = require('undici');
      if (typeof undici.fetch === 'function') fetchFn = undici.fetch;
    } catch (e) {}

    if (!fetchFn) {
      try {
        const mod = await import('node-fetch');
        fetchFn = mod.default || mod.fetch;
      } catch (e) {}
    }
  }

  if (!fetchFn) {
    console.error('No se pudo inicializar fetch. Instala "undici" o "node-fetch": npm i undici node-fetch');
    process.exit(1);
  }

  const fetch = (...args) => fetchFn(...args);

  const app = express();
  app.use(cors());
  app.use(express.json());

  // ------------------------
  // Config Mercado Pago
  // ------------------------
  const MP_ACCESS_TOKEN_FROM_ENV = process.env.MP_ACCESS_TOKEN || '';
  const MP_ACCESS_TOKEN_SANDBOX = process.env.MP_ACCESS_TOKEN_SANDBOX || MP_ACCESS_TOKEN_FROM_ENV || '';
  const MP_ACCESS_TOKEN_PROD = process.env.MP_ACCESS_TOKEN_PROD || '';
  const MP_MODE = (process.env.MP_MODE || 'sandbox').toLowerCase();
  const MP_ACCESS_TOKEN = MP_MODE === 'sandbox' ? MP_ACCESS_TOKEN_SANDBOX : MP_ACCESS_TOKEN_PROD;
  const IS_SANDBOX = MP_MODE === 'sandbox';

  console.log(`🚀 Mercado Pago Mode: ${MP_MODE}`);
  console.log(`🔑 Token usado: ${MP_ACCESS_TOKEN ? MP_ACCESS_TOKEN.slice(0, 10) + '...' : 'NO_TOKEN'}`);

  // ------------------------
  // MEJORADO: Base de datos optimizada con índices y persistencia
  // ------------------------
  let orders = [];
  let payments = [];
  let ordersByStatus = new Map(); // Índice por estado
  let ordersById = new Map(); // Índice por ID
  let lastUpdateTimestamp = Date.now();

  // Persistencia opcional
  const DATA_FILE = path.join(__dirname, 'data.json');
  
  // Cargar datos al iniciar
  async function loadData() {
    try {
      const data = await fs.readFile(DATA_FILE, 'utf8');
      const parsed = JSON.parse(data);
      orders = parsed.orders || [];
      payments = parsed.payments || [];
      rebuildIndexes();
      console.log(`📂 Cargados ${orders.length} pedidos desde archivo`);
    } catch (error) {
      console.log('📂 Iniciando con base de datos vacía');
    }
  }

  // Guardar datos (debounced)
  let saveTimeout = null;
  async function saveData() {
    clearTimeout(saveTimeout);
    saveTimeout = setTimeout(async () => {
      try {
        await fs.writeFile(DATA_FILE, JSON.stringify({ orders, payments }, null, 2));
      } catch (error) {
        console.error('❌ Error guardando datos:', error);
      }
    }, 2000);
  }

  // Reconstruir índices
  function rebuildIndexes() {
    ordersById.clear();
    ordersByStatus.clear();
    
    orders.forEach(order => {
      ordersById.set(order.id, order);
      
      if (!ordersByStatus.has(order.status)) {
        ordersByStatus.set(order.status, []);
      }
      ordersByStatus.get(order.status).push(order);
    });
    
    lastUpdateTimestamp = Date.now();
  }

  await loadData();

  // ------------------------
  // NUEVO: Server-Sent Events para tiempo real
  // ------------------------
  const sseClients = new Set();

  function broadcastToClients(event, data) {
    const message = `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
    sseClients.forEach(client => {
      try {
        client.write(message);
      } catch (error) {
        sseClients.delete(client);
      }
    });
  }

  // Endpoint SSE
  app.get('/events', (req, res) => {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Cache-Control'
    });

    sseClients.add(res);
    console.log(`📡 Cliente SSE conectado (${sseClients.size} total)`);

    // Enviar estado inicial
    res.write(`event: init\ndata: ${JSON.stringify({
      timestamp: lastUpdateTimestamp,
      stats: calculateStats()
    })}\n\n`);

    req.on('close', () => {
      sseClients.delete(res);
      console.log(`📡 Cliente SSE desconectado (${sseClients.size} total)`);
    });
  });

  // ------------------------
  // MEJORADO: Helper con notificaciones
  // ------------------------
  function updateOrderStatus(order, paymentData) {
    const oldStatus = order.status;
    const oldIndex = ordersByStatus.get(oldStatus)?.indexOf(order);
    
    switch ((paymentData.status || '').toString()) {
      case 'approved':
        order.status = 'paid';
        order.payment_id = paymentData.id;
        console.log('✅ Pago aprobado para orden:', order.id);
        break;
      case 'rejected':
      case 'cancelled':
        order.status = 'payment_rejected';
        console.log('❌ Pago rechazado para orden:', order.id);
        break;
      case 'pending':
      case 'in_process':
        order.status = 'pending_payment';
        console.log('⏳ Pago pendiente para orden:', order.id);
        break;
      default:
        console.log('❓ Estado de pago desconocido:', paymentData.status);
    }

    if (oldStatus !== order.status) {
      // Actualizar índices
      if (oldIndex !== -1) {
        ordersByStatus.get(oldStatus).splice(oldIndex, 1);
      }
      
      if (!ordersByStatus.has(order.status)) {
        ordersByStatus.set(order.status, []);
      }
      ordersByStatus.get(order.status).push(order);
      
      lastUpdateTimestamp = Date.now();
      
      console.log(`🔄 Orden ${order.id}: ${oldStatus} → ${order.status}`);
      
      // NUEVO: Notificar cambios en tiempo real
      broadcastToClients('orderUpdate', {
        orderId: order.id,
        oldStatus,
        newStatus: order.status,
        order: order,
        stats: calculateStats()
      });
      
      saveData();
    }
  }

  // Calcular estadísticas optimizado
  function calculateStats() {
    return {
      pending: ordersByStatus.get('pending_payment')?.length || 0,
      paid: ordersByStatus.get('paid')?.length || 0,
      rejected: ordersByStatus.get('payment_rejected')?.length || 0,
      revenue: ordersByStatus.get('paid')?.reduce((sum, o) => sum + o.total, 0) || 0
    };
  }

  // ------------------------
  // MEJORADO: Crear pago con índices
  // ------------------------
  app.post('/create-payment', async (req, res) => {
    try {
      const { items, customer, orderId } = req.body;

      if (!items || !Array.isArray(items) || items.length === 0) {
        return res.status(400).json({ error: 'items required' });
      }
      if (!orderId) {
        return res.status(400).json({ error: 'orderId required' });
      }

      console.log('🛍 Creando pago para:', customer?.name || 'SIN_NOMBRE');

      const total = items.reduce((sum, item) => sum + (parseFloat(item.unit_price || 0) * parseInt(item.quantity || 0)), 0);

      let host = 'http://127.0.0.1:3001';
      if (!IS_SANDBOX) {
        host = process.env.PROD_HOST || 'https://miapp.com';
      }

      const preferenceData = {
        items: items.map(item => ({
          title: item.title || item.name || 'Item',
          unit_price: parseFloat(item.unit_price),
          quantity: parseInt(item.quantity)
        })),
        back_urls: {
          success: `${host}/payment-success`,
          failure: `${host}/payment-failure`,
          pending: `${host}/payment-pending`
        },
        external_reference: orderId
      };

      if (!IS_SANDBOX) preferenceData.auto_return = 'approved';

      console.log('📤 Enviando datos a MP:', JSON.stringify(preferenceData, null, 2));

      const response = await fetch('https://api.mercadopago.com/checkout/preferences', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${MP_ACCESS_TOKEN}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'User-Agent': 'MiApp-Pruebas/1.0 (+https://tuapp.com)'
        },
        body: JSON.stringify(preferenceData)
      });

      console.log('📥 Respuesta MP status:', response.status, response.statusText);

      let responseText = '';
      try {
        responseText = await response.text();
      } catch (e) {
        console.warn('⚠️ Error leyendo body como texto:', e.message);
      }
      console.log('📥 Respuesta MP raw:', responseText && responseText.trim() ? responseText : '<EMPTY>');

      let preference = null;
      if (responseText && responseText.trim() !== '') {
        try {
          preference = JSON.parse(responseText);
        } catch (parseError) {
          console.error('❌ Error parseando JSON manual:', parseError);
        }
      }

      if (!preference) {
        if (response.ok) {
          throw new Error(`MP API returned empty or non-json body but status ${response.status}`);
        } else {
          const details = responseText;
          return res.status(response.status).json({ error: 'MP API Error', details });
        }
      }

      // MEJORADO: Guardar orden con índices
      const order = {
        id: orderId,
        customer,
        items,
        total,
        status: 'pending_payment',
        preference_id: preference.id,
        created_at: new Date().toISOString()
      };
      
      orders.unshift(order); // Añadir al principio
      ordersById.set(order.id, order);
      
      if (!ordersByStatus.has('pending_payment')) {
        ordersByStatus.set('pending_payment', []);
      }
      ordersByStatus.get('pending_payment').unshift(order);
      
      lastUpdateTimestamp = Date.now();

      console.log('✅ Preferencia creada:', preference.id);

      // NUEVO: Notificar nueva orden
      broadcastToClients('newOrder', {
        order: order,
        stats: calculateStats()
      });

      saveData();

      const checkoutUrl = IS_SANDBOX ? (preference.sandbox_init_point || preference.init_point) : preference.init_point;

      return res.json({
        init_point: checkoutUrl,
        preference_id: preference.id,
        order_id: orderId
      });

    } catch (error) {
      console.error('❌ Error creando pago:', error);
      return res.status(500).json({
        error: 'Error creating payment',
        details: error.message
      });
    }
  });

  // ------------------------
  // MEJORADO: Webhook optimizado
  // ------------------------
  app.post('/webhook', async (req, res) => {
    try {
      const { type, data, external_reference, status } = req.body;
      console.log('🔔 Webhook recibido:', { type, data, external_reference, status });

      // Procesar pagos reales
      if (type === 'payment' && data?.id) {
        const paymentId = data.id;

        const paymentResponse = await fetch(`https://api.mercadopago.com/v1/payments/${paymentId}`, {
          headers: { 'Authorization': `Bearer ${MP_ACCESS_TOKEN}` }
        });

        if (paymentResponse.ok) {
          const paymentData = await paymentResponse.json();
          console.log('💰 Datos del pago:', {
            id: paymentData.id,
            status: paymentData.status,
            amount: paymentData.transaction_amount,
            external_reference: paymentData.external_reference
          });

          const order = ordersById.get(paymentData.external_reference);
          if (order) updateOrderStatus(order, paymentData);

          payments.push({
            id: paymentId,
            status: paymentData.status,
            amount: paymentData.transaction_amount,
            order_id: order?.id,
            created_at: new Date().toISOString(),
            external_reference: paymentData.external_reference
          });
        } else {
          console.error('❌ Error consultando pago:', paymentResponse.status);
        }
      }

      // Procesar webhook simulado para testing local
      if (external_reference && status) {
        console.log('🧪 Procesando webhook simulado');
        const order = ordersById.get(external_reference);
        if (order) {
          const mockPaymentData = {
            id: data?.id || `MOCK_${Date.now()}`,
            status: status,
            transaction_amount: order.total,
            external_reference: external_reference
          };
          updateOrderStatus(order, mockPaymentData);

          payments.push({
            id: mockPaymentData.id,
            status: mockPaymentData.status,
            amount: mockPaymentData.transaction_amount,
            order_id: order.id,
            created_at: new Date().toISOString(),
            external_reference: external_reference
          });
        }
      }

      return res.status(200).send('OK');

    } catch (error) {
      console.error('❌ Error procesando webhook:', error);
      return res.status(500).send('Error');
    }
  });

  // ------------------------
  // NUEVOS: Endpoints optimizados con paginación y cache
  // ------------------------
  app.get('/order/:id', (req, res) => {
    const order = ordersById.get(req.params.id);
    if (!order) return res.status(404).json({ error: 'Order not found' });
    return res.json(order);
  });

  app.get('/orders', (req, res) => {
    const { page = 1, limit = 50, status, since } = req.query;
    const pageNum = parseInt(page);
    const limitNum = parseInt(limit);
    
    let filteredOrders = orders;
    
    // Filtrar por estado si se especifica
    if (status && ordersByStatus.has(status)) {
      filteredOrders = ordersByStatus.get(status);
    }
    
    // Filtrar por timestamp para actualizaciones incrementales
    if (since) {
      const sinceTimestamp = parseInt(since);
      filteredOrders = filteredOrders.filter(order => 
        new Date(order.created_at).getTime() > sinceTimestamp
      );
    }
    
    // Paginación
    const startIndex = (pageNum - 1) * limitNum;
    const paginatedOrders = filteredOrders.slice(startIndex, startIndex + limitNum);
    
    return res.json({
      orders: paginatedOrders,
      total: filteredOrders.length,
      page: pageNum,
      limit: limitNum,
      hasMore: startIndex + limitNum < filteredOrders.length,
      timestamp: lastUpdateTimestamp,
      stats: calculateStats()
    });
  });

  // Endpoint solo para estadísticas (muy rápido)
  app.get('/stats', (req, res) => {
    return res.json({
      stats: calculateStats(),
      timestamp: lastUpdateTimestamp
    });
  });

  app.get('/payments', (req, res) => {
    return res.json(payments.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)));
  });

  // ------------------------
  // Páginas de resultado
  // ------------------------
  app.get('/payment-success', (req, res) => {
    res.send(`<h1>✅ Pago Exitoso</h1><p>Tu pedido fue procesado correctamente.</p>`);
  });
  app.get('/payment-failure', (req, res) => {
    res.send(`<h1>❌ Pago Fallido</h1><p>Hubo un problema con tu pago.</p>`);
  });
  app.get('/payment-pending', (req, res) => {
    res.send(`<h1>⏳ Pago Pendiente</h1><p>Tu pago está siendo procesado.</p>`);
  });

  // ------------------------
  // Static + start server
  // ------------------------
  app.use(express.static('public'));
  
  const PORT = process.env.PORT || 3001;
  app.listen(PORT, () => {
    console.log(`🚀 Servidor corriendo en puerto ${PORT}`);
    console.log(`📱 Webhook URL: http://127.0.0.1:${PORT}/webhook`);
    console.log(`📡 SSE Events: http://127.0.0.1:${PORT}/events`);
    console.log(`📊 Stats: http://127.0.0.1:${PORT}/stats`);
  });

  // Cleanup al cerrar
  process.on('SIGINT', () => {
    console.log('\n🛑 Cerrando servidor...');
    clearTimeout(saveTimeout);
    saveData();
    process.exit(0);
  });

  try { module.exports = app; } catch (e) {}
}

init().catch(err => {
  console.error('Fallo iniciando server:', err);
  process.exit(1);
});
// test-token.js
// Script para verificar que tu Access Token funcione correctamente

const MP_ACCESS_TOKEN = 'TEST-7902552494117756-091823-812d2b136fd5ece3d6dfa838a8ed3cc8-145704703'; // TU TOKEN AQUÍ

async function testMercadoPagoToken() {
    console.log('🔍 Probando Access Token...');
    
    try {
        // 1. Verificar el token haciendo una consulta simple
        const response = await fetch('https://api.mercadopago.com/users/me', {
            headers: {
                'Authorization': `Bearer ${MP_ACCESS_TOKEN}`,
                'Content-Type': 'application/json'
            }
        });
        
        const responseText = await response.text();
        console.log('📥 Respuesta status:', response.status);
        console.log('📥 Respuesta:', responseText);
        
        if (!response.ok) {
            console.error('❌ Token inválido o expirado');
            return false;
        }
        
        const userData = JSON.parse(responseText);
        console.log('✅ Token válido! Usuario:', userData.first_name, userData.last_name);
        console.log('🌎 Sitio:', userData.site_id);
        
        return true;
        
    } catch (error) {
        console.error('❌ Error:', error);
        return false;
    }
}

// Función para crear una preferencia de prueba MUY simple
async function testSimplePreference() {
    console.log('\n🧪 Creando preferencia de prueba...');
    
    const minimalPreference = {
        items: [{
            title: 'Pizza Test',
            unit_price: 100,
            quantity: 1
        }]
    };
    
    try {
        const response = await fetch('https://api.mercadopago.com/checkout/preferences', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${MP_ACCESS_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(minimalPreference)
        });
        
        const responseText = await response.text();
        console.log('📤 Enviando:', JSON.stringify(minimalPreference));
        console.log('📥 Status:', response.status);
        console.log('📥 Respuesta:', responseText);
        
        if (response.ok) {
            const preference = JSON.parse(responseText);
            console.log('✅ Preferencia creada!');
            console.log('🔗 Init Point:', preference.init_point);
            return preference;
        } else {
            console.error('❌ Error creando preferencia');
            return null;
        }
        
    } catch (error) {
        console.error('❌ Error:', error);
        return null;
    }
}

// Ejecutar tests
async function runTests() {
    console.log('🚀 Iniciando tests de Mercado Pago...\n');
    
    const tokenValid = await testMercadoPagoToken();
    
    if (tokenValid) {
        await testSimplePreference();
    }
    
    console.log('\n✨ Tests completados');
}

// Si ejecutas este archivo directamente
if (require.main === module) {
    runTests();
}

module.exports = { testMercadoPagoToken, testSimplePreference };
# src/controllers/health_check.py
from flask import Blueprint, jsonify
from src.config.database import db
from src.models.User import User  # Importa tu modelo
from sqlalchemy import text
import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
def health_check():
    """Endpoint básico de salud"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'service': 'PioCrokanti API'
    }), 200

@health_bp.route('/db', methods=['GET'])
def database_health_check():
    """Verificación completa de la base de datos"""
    result = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'database': {}
    }
    
    try:
        # Test 1: Conexión básica
        db.session.execute(text('SELECT 1'))
        result['database']['connection'] = 'ok'
        
        # Test 2: Verificar que existe la tabla users
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'users' in tables:
            result['database']['table_users'] = 'exists'
            
            # Test 3: Contar registros en users
            user_count = User.query.count()
            result['database']['users_count'] = user_count
            
            # Test 4: Test de escritura/lectura (opcional)
            try:
                # Crear un usuario de prueba temporalmente
                import random
                test_phone = f'TEST_{random.randint(100000, 999999)}'  # Máximo 11 caracteres
                test_user = User(
                    nombre='Test',
                    apellido='Health',
                    telefono=test_phone,
                    direccion='Test Address'
                )
                db.session.add(test_user)
                db.session.commit()
                
                # Leer el usuario
                found_user = User.query.filter_by(nombre='Test', apellido='Health').first()
                
                if found_user:
                    result['database']['read_write'] = 'ok'
                    # Limpiar - eliminar el usuario de prueba
                    db.session.delete(found_user)
                    db.session.commit()
                else:
                    result['database']['read_write'] = 'error'
                    
            except Exception as e:
                result['database']['read_write'] = f'error: {str(e)}'
                db.session.rollback()
        else:
            result['database']['table_users'] = 'missing'
            result['database']['error'] = 'Table users does not exist'
        
        # Test 5: Info de la base de datos
        db_info = db.session.execute(text('SELECT version()')).scalar()
        result['database']['version'] = db_info
        
        result['status'] = 'healthy'
        status_code = 200
        
    except Exception as e:
        result['status'] = 'unhealthy'
        result['database']['error'] = str(e)
        result['database']['connection'] = 'failed'
        status_code = 503
        
    finally:
        db.session.close()
    
    return jsonify(result), status_code

@health_bp.route('/db/simple', methods=['GET'])
def simple_database_check():
    """Verificación simple y rápida"""
    try:
        # Solo verificar conexión
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'ok',
            'database': 'connected',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 503

@health_bp.route('/db/tables', methods=['GET'])
def check_tables():
    """Verificar qué tablas existen"""
    try:
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        return jsonify({
            'status': 'ok',
            'tables': tables,
            'tables_count': len(tables),
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 503
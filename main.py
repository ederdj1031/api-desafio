from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from transform_info import transform_info
from user import User
import mysql.connector

app = FastAPI()


# permisos de política de seguridad CORS habilitados para cualquier origen
origins = [
    "*"
] 

token_global = "123456789456123456789"

def verificar_token(token: str = Header(...)):
    if token != token_global:  
        raise HTTPException(status_code=401, detail="Token no válido")
    return token

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

users_data_schema = list(User.model_json_schema()["properties"].keys())

# EndPoint de prueba
@app.get("/")
async def index():
    return {
        "message" : "Api en funcionamiento correcto",
        "status" : 200
    }
    
# EndPoint para extraer todos los registros de la base de datos
@app.get("/all")
async def show_all(token: str = Depends(verificar_token)):
    
    print(token)
    
    try:
        connection = mysql.connector.connect(
            host='integra2db.cdygn8mgmkud.us-east-1.rds.amazonaws.com',
            user='erios',
            password='Qazplm123!',
            database='users'
        )
        cursor = connection.cursor()
        # Consulta SQL
        cursor.execute("SELECT * FROM users.users_info")
        columns = [col[0] for col in cursor.description]
        resp = transform_info(cursor.fetchall(), columns)

        # Cierre de conexiones
        cursor.close()
        connection.close()
        
        return{
                "message": "Conexión exitosa",
                "status": "200",
                "response": resp
            }
    
    # Manejar y retornar cualquier error
    except:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="Bad request")
        
# EndPoint para obtener un usuario por su ID
@app.get("/id/{id}")
def show_user_by_id(id, token: str = Depends(verificar_token)):
    try:
        connection = mysql.connector.connect(
            host='integra2db.cdygn8mgmkud.us-east-1.rds.amazonaws.com',
            user='erios',
            password='Qazplm123!',
            database='users'
        )
        
        cursor = connection.cursor()
        
        # Consulta SQL
        cursor.execute(f"SELECT * FROM users.users_info WHERE id = {id}")
        columns = [col[0] for col in cursor.description]
        resp = transform_info(cursor.fetchall(), columns)
        
        if(resp == []):
            raise HTTPException(
                status_code= 404,
                detail = "usuario no encontrado"
            )
        
        # Cierre de conexiones
        cursor.close()
        connection.close()
        return{
                "message": "Usuario encontrado",
                "status": "200",
                "response": resp
            }

    # Manejar y retornar cualquier error
    except:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="Bad request")

# EndPoint para agregar un usuario 

@app.post("/add")
def add_user(user: User, token: str = Depends(verificar_token)):
    # IMPORTANTE debe venir como un archivo JSON el cuerpo de la opeticion post, 
    # vease User para ver como debe ir la infomación.
    try:
        connection = mysql.connector.connect(
            host='integra2db.cdygn8mgmkud.us-east-1.rds.amazonaws.com',
            user='erios',
            password='Qazplm123!',
            database='users'
        )
        
        cursor = connection.cursor()
        
        sentencia = "INSERT INTO users.users_info ("
        for data in users_data_schema:
            sentencia += f"{data},"   
        sentencia += ")"

        sentencia += " VALUES("
        for data in user.getData():
            if isinstance(data, str):
                sentencia += f'"{data}",'   
            elif isinstance(data, int):
                sentencia += f"{data},"
            else:
                raise HTTPException(status_code=400, detail="Bad request, errorType")
            
        sentencia += ")"    
        sentencia=sentencia.replace(",)", ")")
        
        # Consulta SQL
        cursor.execute(sentencia)
        
        # En caso de no haber errores en la base de datos, aplicamos cambios 
        connection.commit()
        
        # Cierre de conexiones
        cursor.close()
        connection.close()
        return {
            "message":"inserción completa",
            "status": "200",
        }
    
    # Manejar y retornar cualquier error
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail=str(error))
    
    except:
        raise HTTPException(status_code=400, detail="Bad request")
        
# EndPoint para eliminar un usuario por su ID
@app.delete("/delete/{id}")
def delete_user(id, token: str = Depends(verificar_token)):
    try:
        connection = mysql.connector.connect(
            host='integra2db.cdygn8mgmkud.us-east-1.rds.amazonaws.com',
            user='erios',
            password='Qazplm123!',
            database='users'
        )
        
        cursor = connection.cursor()
        
        # Consulta SQL
        cursor.execute(F'DELETE FROM users.users_info WHERE id = {id};')
        
        # En caso de no haber errores en la base de datos, aplicamos cambios 
        connection.commit()
        
        # Cierre de conexiones
        cursor.close()
        connection.close()
        
        return{
            "message": f"usuario con id {id} eliminado",
            "status": "200",
        }
    
    # Manejar y retornar cualquier error de SQL
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Manejar y retornar cualquier error desconocido
    except Exception as ex:
        raise HTTPException(status_code=400, detail="Bad request")


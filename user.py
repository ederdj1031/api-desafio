from pydantic import BaseModel

class User(BaseModel):
    fec_alta: str
    user_name: str
    codigo_zip: str
    credit_card_num: str
    credit_card_ccv: str
    cuenta_numero: str
    direccion: str
    geo_latitud: str
    geo_longitud: str
    color_favorito: str
    foto_dni: str
    ip: str
    auto: str
    auto_modelo: str
    auto_tipo: str
    auto_color: str
    cantidad_compras_realizadas: int
    avatar: str
    fec_birthday: str
    id: int
    
    def getData(self):
        return[
          self.fec_alta,
          self.user_name,
          self.codigo_zip,
          self.credit_card_num,
          self.credit_card_ccv,
          self.cuenta_numero,
          self.direccion,
          self.geo_latitud,
          self.geo_longitud,
          self.color_favorito,
          self.foto_dni,
          self.ip,
          self.auto,
          self.auto_modelo,
          self.auto_tipo,
          self.auto_color,
          self.cantidad_compras_realizadas,
          self.avatar,
          self.fec_birthday,
          self.id
        ]
from db import db


class HotelModel(db.Model):
    __tablename__ = 'hoteis'

    # definindo as colunas do banco
    hotel_id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String(255))
    estrelas = db.Column(db.Float(precision=1))     # precision= qtd de casas depois da virgula
    diaria = db.Column(db.Float(precision=2))
    cidade = db.Column(db.String(50))
    site_id = db.Column(db.Integer, db.ForeignKey('sites.site_id'))
    # site = db.relationship('SiteModel')  acesso ao site que oferta esse hotel

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id

    def json(self):
        return {
            "hotel_id": self.hotel_id,
            "nome": self.nome,
            "estrelas": self.estrelas,
            "diaria": self.diaria,
            "cidade": self.cidade,
            "site_id": self.site_id
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()  # SELECT * FROM hoteis WHERE hotel_id=hotel_id
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        db.session.add(self)
        db.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        db.session.delete(self)
        db.session.commit()

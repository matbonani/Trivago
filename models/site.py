from db import db


class SiteModel(db.Model):
    __tablename__ = 'sites'

    # definindo as colunas do banco
    site_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    hoteis = db.relationship('HotelModel')   # Lista de objetos hoteis

    def __init__(self, url):
        self.url = url

    def json(self):
        return {
            "site_id": self.site_id,
            "url": self.url,
            "hoteis": [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first()  # SELECT * FROM hoteis WHERE hotel_id=hotel_id
        if site:
            return site
        return None

    def save_site(self):
        db.session.add(self)
        db.session.commit()

    def delete_site(self):
        db.session.delete(self)
        db.session.commit()

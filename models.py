# models.py

from backups.app import db


class HumanData(db.Model):
    __tablename__ = "human_data"

    id = db.Column(db.BigInteger, primary_key=True)
    states = db.Column(db.String(20), nullable=False)
    season_description = db.Column(db.String(20), nullable=False)
    flu_pdm = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<HumanData: {}>'.format(self.states)

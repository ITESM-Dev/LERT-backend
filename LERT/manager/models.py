from LERT.db.database import db


class Manager(db.Model):
    __tablename__ = "Manager"

    idManager = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey("User.idUser"))
    idOPManager = db.Column(db.Integer, db.ForeignKey("OpManager.idOPManager"))
    idICA_Admin = db.Column(db.Integer, db.ForeignKey("ICAAdmin.idICA_Admin"))

    user = db.relationship("User", back_populates="manager")
    expense = db.relationship("Expense")
    
from FlaskAPP import db

class Doctor(db.Model):
    __tablename__ = 'Doctor'
    __table_args__ = {'extend_existing': True}
    DoctorID = db.Column(db.Integer, primary_key=True)
    DoctorName = db.Column(db.String(50))
    email = db.Column(db.String(50), primary_key=True)
    password_ = db.Column(db.String(15))
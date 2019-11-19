from FlaskAPP import db

class Pressure(db.Model):
    TestID = db.Column(db.Integer, db.ForeignKey('testframe.TestID'), 
        primary_key=True)
    CircleID = db.Column(db.Integer, db.ForeignKey('circles.CircleID'), 
        primary_key=True)
    PressureID = db.Column(db.Integer, primary_key=True)
    Xcoord = db.Column(db.Float)
    Ycoord = db.Column(db.Float)
    Pressure = db.Column(db.Float)
    
    
from fitness.models import *
import base64
import hashlib
import os


def create_users (a_email, a_username, a_password, a_gender, a_age, a_weight,
                a_height, a_athlete, a_heart_disease, a_smoking, a_medical_implant,
                a_target=None):
    a_secure_token = base64.urlsafe_b64encode(os.urandom(16)).rstrip(b'=').decode('ascii')
    a_password = hashlib.sha256(str(a_password).encode('utf-8')).hexdigest()
    user = UserAccounts(
                        username=a_username, email=a_email, password=a_password,
                        secure_token=a_secure_token, gender=a_gender, age=a_age,
                        weight=a_weight, height=a_height, athlete=a_athlete,
                        heart_disease=a_heart_disease, smoking=a_smoking,
                        medical_implant=a_medical_implant, training_target=a_target
                        )
    user.email_verified = 1 #require verification first
    user.save()


# create_users("a@a", "aaaa", "1111", "M", 18, 60.0, 175.0, False, False, False, False)
# create_users("b@b", "bbbb", "1111", "M", 18, 60.0, 175.0, False, False, False, False)
# create_users("c@c", "cccc", "1111", "M", 18, 60.0, 175.0, False, False, False, False)
# create_users("d@d", "dddd", "1111", "M", 18, 60.0, 175.0, False, False, False, False)
# create_users("e@e", "eeee", "1111", "M", 18, 60.0, 175.0, False, False, False, False)
# create_users("f@f", "ffff", "1111", "M", 18, 60.0, 175.0, False, False, False, False)
# create_users("g@g", "gggg", "1111", "M", 18, 60.0, 175.0, False, False, False, False)
# create_users("h@h", "hhhh", "1111", "M", 25, 60.0, 175.0, False, False, False, False)
# create_users("i@i", "iiii", "1111", "M", 25, 60.0, 175.0, False, False, False, False)
# create_users("j@j", "jjjj", "1111", "M", 25, 60.0, 175.0, False, False, False, False)
# create_users("k@k", "kkkk", "1111", "M", 25, 60.0, 175.0, False, False, False, False)
# create_users("l@l", "llll", "1111", "M", 25, 60.0, 175.0, False, False, False, False)
# create_users("m@m", "mmmm", "1111", "M", 25, 60.0, 175.0, False, False, False, False)
# create_users("n@n", "nnnn", "1111", "F", 18, 60.0, 175.0, True, False, False, False)
# create_users("o@o", "oooo", "1111", "F", 18, 60.0, 175.0, True, False, False, False)
# create_users("p@p", "pppp", "1111", "F", 18, 60.0, 175.0, True, False, False, False)
# create_users("q@q", "qqqq", "1111", "F", 18, 60.0, 175.0, True, False, False, False)
# create_users("r@r", "rrrr", "1111", "F", 18, 60.0, 175.0, True, False, False, False)
# create_users("s@s", "ssss", "1111", "F", 18, 60.0, 175.0, True, False, False, False)
# create_users("t@t", "tttt", "1111", "F", 25, 60.0, 175.0, True, False, False, False)
# create_users("u@u", "uuuu", "1111", "F", 25, 60.0, 175.0, True, False, False, False)
# create_users("v@v", "vvvv", "1111", "F", 25, 60.0, 175.0, True, False, False, False)
# create_users("w@w", "wwww", "1111", "F", 25, 60.0, 175.0, True, False, False, False)
# create_users("x@x", "xxxx", "1111", "F", 25, 60.0, 175.0, True, False, False, False)
# create_users("y@y", "yyyy", "1111", "F", 25, 60.0, 175.0, True, False, False, False)
# create_users("z@z", "zzzz", "1111", "F", 25, 60.0, 175.0, True, False, False, False)
# create_users("test@test", "test", "test", "M", 25, 60.0, 175.0, True, False, False, False, "Chest")

create_users(a_email="a@a", a_username="aaaa", a_password="1111", a_gender="M", a_age=18, a_weight=60.0, a_height=160.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="b@b", a_username="bbbb", a_password="1111", a_gender="M", a_age=18, a_weight=60.0, a_height=160.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="c@c", a_username="cccc", a_password="1111", a_gender="M", a_age=18, a_weight=60.0, a_height=190.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="d@d", a_username="dddd", a_password="1111", a_gender="M", a_age=18, a_weight=60.0, a_height=190.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="e@e", a_username="eeee", a_password="1111", a_gender="M", a_age=18, a_weight=80.0, a_height=160.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="f@f", a_username="ffff", a_password="1111", a_gender="M", a_age=18, a_weight=80.0, a_height=190.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="g@g", a_username="gggg", a_password="1111", a_gender="M", a_age=18, a_weight=80.0, a_height=190.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="h@h", a_username="hhhh", a_password="1111", a_gender="M", a_age=30, a_weight=60.0, a_height=160.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="i@i", a_username="iiii", a_password="1111", a_gender="M", a_age=30, a_weight=60.0, a_height=160.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="j@j", a_username="jjjj", a_password="1111", a_gender="M", a_age=30, a_weight=60.0, a_height=190.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="k@k", a_username="kkkk", a_password="1111", a_gender="M", a_age=30, a_weight=80.0, a_height=160.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="l@l", a_username="llll", a_password="1111", a_gender="M", a_age=30, a_weight=80.0, a_height=160.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="m@m", a_username="mmmm", a_password="1111", a_gender="M", a_age=30, a_weight=80.0, a_height=190.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="n@n", a_username="nnnn", a_password="1111", a_gender="F", a_age=18, a_weight=60.0, a_height=160.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="o@o", a_username="oooo", a_password="1111", a_gender="F", a_age=18, a_weight=60.0, a_height=160.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="p@p", a_username="pppp", a_password="1111", a_gender="F", a_age=18, a_weight=60.0, a_height=190.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="q@q", a_username="qqqq", a_password="1111", a_gender="F", a_age=18, a_weight=60.0, a_height=190.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="r@r", a_username="rrrr", a_password="1111", a_gender="F", a_age=18, a_weight=80.0, a_height=160.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="s@s", a_username="ssss", a_password="1111", a_gender="F", a_age=18, a_weight=80.0, a_height=190.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="t@t", a_username="tttt", a_password="1111", a_gender="F", a_age=18, a_weight=80.0, a_height=190.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="u@u", a_username="uuuu", a_password="1111", a_gender="F", a_age=30, a_weight=60.0, a_height=160.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="v@v", a_username="vvvv", a_password="1111", a_gender="F", a_age=30, a_weight=60.0, a_height=160.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="w@w", a_username="wwww", a_password="1111", a_gender="F", a_age=30, a_weight=60.0, a_height=190.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="x@x", a_username="xxxx", a_password="1111", a_gender="F", a_age=30, a_weight=80.0, a_height=160.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="y@y", a_username="yyyy", a_password="1111", a_gender="F", a_age=30, a_weight=80.0, a_height=160.0, a_athlete=False, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="z@z", a_username="zzzz", a_password="1111", a_gender="F", a_age=30, a_weight=80.0, a_height=190.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Chest")
create_users(a_email="test@test", a_username="test", a_password="1111", a_gender="M", a_age=18, a_weight=60.0, a_height=160.0, a_athlete=True, a_heart_disease=False, a_smoking=False, a_medical_implant=False, a_target="Butt")

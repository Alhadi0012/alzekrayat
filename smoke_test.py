"""End-to-end check of every feature using Flask's test client."""
import io, os
from PIL import Image
from app import createApp

if os.path.exists("alzikrayat.db"): os.remove("alzikrayat.db")
app = createApp()
c1, c2 = app.test_client(), app.test_client()

def img(name):
    buf = io.BytesIO(); Image.new("RGB",(60,60),(200,30,30)).save(buf,"PNG"); buf.seek(0)
    return (buf, name)

ok = lambda label, cond: print(("PASS " if cond else "FAIL ") + label)

# 1 home + about + 404 + 405
ok("home page", b"Alzikrayat" in c1.get("/").data)
ok("about page", b"About Alzikrayat" in c1.get("/about").data)
ok("404 unknown route", c1.get("/no-such-page").status_code == 404)
ok("405 wrong method", c1.get("/photo/store").status_code == 405)

# 2 register validation + success
bad = c1.post("/register", data={"firstName":"A1","lastName":"","email":"bad","password":"12"})
ok("server-side validation blocks bad register", b"valid email" in bad.data)
r = c1.post("/register", data={"firstName":"Hadeep","lastName":"Ali",
    "email":"hadeep@sust.edu","password":"secret123","location":"Khartoum",
    "description":"student","occupation":"developer"}, follow_redirects=True)
ok("register + auto login", b"Hi Hadeep" in r.data)

# 3 password never stored raw
with app.app_context():
    from app.models.user import User
    u = User.findByEmail("hadeep@sust.edu")
ok("password hashed", "secret123" not in u["password"] and len(u["password"]) > 40)

# 4 logout / login / cookie
ok("logout", b"Please Login" in c1.get("/logout", follow_redirects=True).data)
ok("wrong password rejected", b"Invalid email" in c1.post("/login",
    data={"email":"hadeep@sust.edu","password":"wrong"}).data)
login = c1.post("/login", data={"email":"hadeep@sust.edu","password":"secret123"})
ok("last-login cookie set", "lastLogin" in login.headers.get("Set-Cookie",""))
ok("cookie shown on login page", b"Last login from this computer" in c1.get("/login").data)

# 5 upload
up = c1.post("/photo/store", data={"title":"Nile Sunset","description":"Evening in Khartoum",
    "photo": img("nile.png")}, content_type="multipart/form-data", follow_redirects=True)
ok("upload photo", b"uploaded successfully" in up.data)
with app.app_context():
    from app.models.photo import Photo
    photo = Photo.all()[0]
ok("file saved on disk", os.path.exists(os.path.join("app/static/uploads", photo["file_name"])))
ok("bad file type rejected", b"Only PNG" in c1.post("/photo/store",
    data={"title":"x","photo":(io.BytesIO(b"x"),"virus.exe")},
    content_type="multipart/form-data").data)

# 6 gallery styles + detail
ok("gallery grid3", b"Nile Sunset" in c1.get("/photos?style=grid3").data)
ok("gallery grid4", b"col-6 col-md-3" in c1.get("/photos?style=grid4").data)
ok("gallery list",  b"list-group-item" in c1.get("/photos?style=list").data)
detail = c1.get("/photo/%d" % photo["id"])
ok("detail view (regex param)", b"Evening in Khartoum" in detail.data)
ok("missing photo 404", c1.get("/photo/9999").status_code == 404)

# 7 comments
ok("guest cannot comment", b"Please login" in c2.post("/photo/%d/comment" % photo["id"],
    data={"comment":"hi"}, follow_redirects=True).data)
cm = c1.post("/photo/%d/comment" % photo["id"], data={"comment":"Beautiful shot!"},
             follow_redirects=True)
ok("comment added and displayed", b"Beautiful shot!" in cm.data)

# 8 XSS escaped
c1.post("/photo/%d/comment" % photo["id"], data={"comment":"<script>alert(1)</script>"})
ok("XSS escaped in output", b"<script>alert(1)</script>" not in c1.get("/photo/%d" % photo["id"]).data)

# 9 ownership check on delete
c2.post("/register", data={"firstName":"Sara","lastName":"Omer",
    "email":"sara@sust.edu","password":"secret123"})
other = c2.post("/photo/%d/delete" % photo["id"], follow_redirects=True)
ok("cannot delete another user's photo", b"only delete your own" in other.data)
with app.app_context():
    ok("photo still exists", Photo.findById(photo["id"]) is not None)

mine = c1.post("/photo/%d/delete" % photo["id"], follow_redirects=True)
ok("owner can delete", b"Photo deleted" in mine.data)
with app.app_context():
    gone = Photo.findById(photo["id"])
    from app.models.comment import Comment
    cascade = Comment.findByPhoto(photo["id"])
ok("row deleted", gone is None)
ok("comments cascade deleted", cascade == [])
ok("file removed from disk", not os.path.exists(os.path.join("app/static/uploads", photo["file_name"])))

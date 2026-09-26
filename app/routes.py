"""
Flat URL table.
Every path is registered here and resolved by our own regex Router,
never by Flask's routing system.
"""
from app.core.router import Router
from app.controllers.home_controller import HomeController
from app.controllers.auth_controller import AuthController
from app.controllers.photo_controller import PhotoController
from app.controllers.comment_controller import CommentController

router = Router()

# Public pages
router.add("GET", "/", HomeController.index)
router.add("GET", "/about", HomeController.about)

# Authentication
router.add("GET", "/register", AuthController.showRegister)
router.add("POST", "/register", AuthController.register)
router.add("GET", "/login", AuthController.showLogin)
router.add("POST", "/login", AuthController.login)
router.add("GET", "/logout", AuthController.logout)

# Photos (note the parameterized paths captured by regex)
router.add("GET", "/photos", PhotoController.index)
router.add("GET", "/photo/new", PhotoController.create)
router.add("POST", "/photo/store", PhotoController.store)
router.add("GET", "/photo/{id:int}", PhotoController.show)
router.add("POST", "/photo/{id:int}/delete", PhotoController.delete)

# Comments
router.add("POST", "/photo/{id:int}/comment", CommentController.store)

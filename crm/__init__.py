from flask import Flask

def create_app():
    app = Flask(__name__)

    # 블루프린트
    from .views import main, user, store, item, order, orderitem

    app.register_blueprint(main.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(store.bp)
    app.register_blueprint(item.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(orderitem.bp)

    return app
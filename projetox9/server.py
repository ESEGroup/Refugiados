from projetox9 import app, Config
app.run(host=Config.projetox9_url.host, port=Config.projetox9_url.port, debug=True)

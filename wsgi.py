from motonaut import app, socketio


if __name__ == "__main__":
    #app.run(debug=True)
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
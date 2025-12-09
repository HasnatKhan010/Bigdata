from __future__ import annotations

import uuid
from dataclasses import asdict
from typing import List

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit

from config import settings
from models import Driver, DriverStatus, Location, Order, OrderStatus
from algorithms import (
    run_astar,
    run_genetic,
    run_greedy,
    run_ucs,
    run_csp,
    run_hill_climbing,
    run_bfs,
)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    return app


app = create_app()
socketio = SocketIO(
    app,
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
    message_queue=settings.SOCKET_MESSAGE_QUEUE,
    async_mode="eventlet",
)

orders: List[Order] = []
drivers: List[Driver] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/orders")
def list_orders():
    return jsonify([asdict(o) for o in orders])


@app.post("/orders")
def create_order():
    data = request.json or {}
    new_order = Order(
        id=str(uuid.uuid4()),
        customer=data.get("customer", "Anonymous"),
        pickup=Location(**data.get("pickup", {"lat": 33.6844, "lng": 73.0479})),
        dropoff=Location(**data.get("dropoff", {"lat": 33.7294, "lng": 73.0931})),
        priority=data.get("priority", "standard"),
    )
    orders.append(new_order)
    socketio.emit("order_created", asdict(new_order))
    return asdict(new_order), 201


@socketio.on("connect")
def handle_connect():
    emit("sync_state", {"orders": [asdict(o) for o in orders], "drivers": [asdict(d) for d in drivers]})


@socketio.on("request_route")
def handle_route(data):
    start = data.get("start")
    goal = data.get("goal")
    graph = data.get("graph", {})
    route = run_astar(start, goal, graph)
    emit("route_response", route)


def seed_drivers():
    if drivers:
        return
    base_location = Location(33.6844, 73.0479)
    for i in range(3):
        drivers.append(
            Driver(
                id=str(uuid.uuid4()),
                name=f"Driver {i+1}",
                vehicle_type="bike",
                location=base_location,
                status=DriverStatus.AVAILABLE,
            )
        )


if __name__ == "__main__":
    seed_drivers()
    socketio.run(app, host="0.0.0.0", port=5000)

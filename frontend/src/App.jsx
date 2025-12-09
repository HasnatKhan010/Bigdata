import { useEffect, useMemo, useState } from "react";
import { io } from "socket.io-client";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "./App.css";

const ISLAMABAD = { lat: 33.6844, lng: 73.0479 };

const socket = io("http://localhost:5000", {
  autoConnect: true,
  transports: ["websocket", "polling"],
});

function App() {
  const [orders, setOrders] = useState([]);
  const [drivers, setDrivers] = useState([]);

  useEffect(() => {
    socket.on("sync_state", (payload) => {
      setOrders(payload.orders ?? []);
      setDrivers(payload.drivers ?? []);
    });
    socket.on("order_created", (order) => {
      setOrders((prev) => [...prev, order]);
    });
    return () => {
      socket.off("sync_state");
      socket.off("order_created");
    };
  }, []);

  const center = useMemo(() => [ISLAMABAD.lat, ISLAMABAD.lng], []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <header className="border-b border-slate-800 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">Real-Time Delivery (Islamabad)</h1>
          <p className="text-sm text-slate-400">Live orders, drivers, and AI routing stubs</p>
        </div>
        <div className="flex gap-4 text-sm text-slate-300">
          <span>Orders: {orders.length}</span>
          <span>Drivers: {drivers.length}</span>
        </div>
      </header>

      <main className="flex-1 grid md:grid-cols-3">
        <div className="md:col-span-2 border-r border-slate-800">
          <MapContainer center={center} zoom={12} className="h-full w-full">
            <TileLayer
              attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {drivers.map((driver) => (
              <Marker key={driver.id} position={[driver.location.lat, driver.location.lng]}>
                <Popup>
                  <div className="space-y-1">
                    <div className="font-semibold">{driver.name}</div>
                    <div className="text-xs text-slate-600">Vehicle: {driver.vehicle_type}</div>
                    <div className="text-xs text-slate-600">Status: {driver.status}</div>
                  </div>
                </Popup>
              </Marker>
            ))}
            {orders.map((order) => (
              <Marker key={order.id} position={[order.dropoff.lat, order.dropoff.lng]}>
                <Popup>
                  <div className="space-y-1">
                    <div className="font-semibold">{order.customer}</div>
                    <div className="text-xs text-slate-600">Priority: {order.priority}</div>
                    <div className="text-xs text-slate-600">Status: {order.status}</div>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>

        <div className="p-6 space-y-4">
          <section>
            <h2 className="text-lg font-semibold">Algorithms</h2>
            <p className="text-sm text-slate-400">
              Backend exposes stubs for A*, Genetic, Greedy, UCS, CSP, Hill Climbing, and BFS.
            </p>
          </section>
          <section className="space-y-2">
            <h3 className="text-sm font-semibold text-slate-200">Live Feed</h3>
            <div className="text-xs text-slate-400 bg-slate-900/60 rounded-lg p-3 border border-slate-800 h-64 overflow-auto">
              {orders.length === 0 ? (
                <p>No orders yet. POST to /orders on backend to stream updates.</p>
              ) : (
                orders.map((order) => (
                  <div key={order.id} className="mb-2">
                    <div className="font-semibold text-slate-200">{order.customer}</div>
                    <div className="text-slate-400">
                      {order.status} · priority {order.priority}
                    </div>
                  </div>
                ))
              )}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;

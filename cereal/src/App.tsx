import CerealSidebar from "./components/CerealSidebar";
import CerealRoutes from "./navigation";

export default function App() {
  return (
    <div className="flex">
      <CerealSidebar />
      <CerealRoutes />
    </div>
  );
}

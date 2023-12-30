import { Bluetooth, Mqtt, Usb, Wifi } from "@/pages";
import { Route, Routes } from "react-router-dom";

const CerealRoutes = () => {
  return (
    <Routes>
      <Route path="/usb" element={<Usb />} />
      <Route path="/mqtt" element={<Mqtt />} />
      <Route path="/wifi" element={<Wifi />} />
      <Route path="/bluetooth" element={<Bluetooth />} />
    </Routes>
  );
};

export default CerealRoutes;

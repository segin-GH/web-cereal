import { Bluetooth, Mqtt, Usb, Wifi } from "@/pages";
import { BrowserRouter, Route, Routes } from "react-router-dom";

const CerealRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/usb" element={<Usb />} />
        <Route path="/mqtt" element={<Mqtt />} />
        <Route path="/wifi" element={<Wifi />} />
        <Route path="/bluetooth" element={<Bluetooth />} />
      </Routes>
    </BrowserRouter>
  );
};

export default CerealRoutes;

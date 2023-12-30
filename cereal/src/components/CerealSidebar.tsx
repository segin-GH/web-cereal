import { useEffect, useState } from "react";

import { Link } from "react-router-dom";
import { FaUsb } from "react-icons/fa";
import {
  MdSignalWifiStatusbar3Bar,
  MdBluetoothSearching,
} from "react-icons/md";
import { SiMqtt } from "react-icons/si";
import { useLocation } from "react-router-dom";

const style = {
  color: "#676756",
  fontSize: "1em",
};

function CerealSidebar() {
  return (
    <div className="flex h-screen w-12">
      <nav>
        <NavItems />
      </nav>
    </div>
  );
}

export default CerealSidebar;

const navMenu = [
  {
    icon: <FaUsb style={style} />,
    link: "/usb",
  },
  {
    icon: <MdSignalWifiStatusbar3Bar style={style} />,
    link: "/wifi",
  },
  {
    icon: <MdBluetoothSearching style={style} />,
    link: "/bluetooth",
  },
  {
    icon: <SiMqtt style={style} />,
    link: "/mqtt",
  },
];

const NavItems = () => {
  const location = useLocation();
  const [active, setActive] = useState(location.pathname);
  useEffect(() => {
    setActive(location.pathname);
  }, [location]);

  return (
    <ul className="flex-col text-clr-text font-bold bg-clr-bg-prim w-12 h-[calc(100vh)]">
      {navMenu.map((item, index) => (
        <li key={index}>
          <Link
            to={item.link}
            className="flex justify-center items-center h-12 "
            style={{
              backgroundColor: active === item.link ? "#ffccdd" : "",
              borderRadius: "4px",
              marginBottom: "4px",
            }}
          >
            {item.icon}
          </Link>
        </li>
      ))}
    </ul>
  );
};

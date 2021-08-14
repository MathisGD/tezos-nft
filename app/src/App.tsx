import './App.css';
import Navbar from './components/Navbar.js'
import Bridge from './components/Bridge.js'
import { MetaMaskProvider } from 'metamask-react'
import React, { useState } from "react";
import { TezosToolkit } from "@taquito/taquito";
import ConnectButton from "./components/ConnectWallet";




function App() {
  const [Tezos, setTezos] = useState<TezosToolkit>(
    new TezosToolkit("https://api.tez.ie/rpc/granadanet")
  );
  const [contract, setContract] = useState<any>(undefined);
  const [publicToken, setPublicToken] = useState<string | null>("");
  const [wallet, setWallet] = useState<any>(null);
  const [userAddress, setUserAddress] = useState<string>("");
  const [userBalance, setUserBalance] = useState<number>(0);
  const [storage, setStorage] = useState<number>(0);
  const [copiedPublicToken, setCopiedPublicToken] = useState<boolean>(false);
  const [beaconConnection, setBeaconConnection] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>("transfer");

    return (
    <div className="App">
        <MetaMaskProvider>
          <ConnectButton
            Tezos={Tezos}
            setContract={setContract}
            setPublicToken={setPublicToken}
            setWallet={setWallet}
            setUserAddress={setUserAddress}
            setUserBalance={setUserBalance}
            setStorage={setStorage}
            
            setBeaconConnection={setBeaconConnection}
            wallet={wallet}
          />
            <header className="App-header">
                <Navbar />
                <div className="Content">
                    <Bridge />
                </div>
            </header>
        </MetaMaskProvider>
    </div>
  );
}

export default App;

import React from 'react';
import styles from './navbar.module.css'
import { ReactComponent as Logo } from '../static/bridge.svg';
import EthereumButton from "./MetamaskButton";
import ThemeSwitch from "./ThemeSwitch";

class Navbar extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            collapse: false,
        };
    }


    render() {
        return (
            <div className={`${styles.navbar} navbar`} >
                <Logo className={styles.icon} fill='var(--text-color)' />
                <EthereumButton />
                <ThemeSwitch/>
            </div >
        )
    }
}

export default Navbar;

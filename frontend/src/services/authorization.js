import React, { createContext, useState, useEffect } from "react";

import { universalLogin } from '../apis/medblock';
import { isValidAuthority } from '../utils/authorityTypesValidator';

const AuthContext = createContext({});

const AuthProvider = (props) => {

  const [loggedIn, setLoggedIn] = useState(false);
  const [wallet, setWallet] = useState(undefined);
  const [authority, setAuthority] = useState(undefined);
  const [entityInfo, setEntityInfo] = useState(undefined);

  useEffect(() => {
    // Pull saved login state from localStorage
    const pk = localStorage.getItem('pk');
    const authorityType = localStorage.getItem('authorityType');

    console.log("Validate", pk, authorityType);
    if(!isValidAuthority(authorityType)){
      console.log("Localstorage compromised !!!");
      console.log("Resetting the localstorage for security reasons, Login again please :)");
      // localStorage.clear();
      return false;
    }

    universalLogin(pk, authorityType)
      .then(info => {
        setEntityInfo(info);
        setAuthority(authorityType);
        setLoggedIn(true);

        console.log("Initial login successful with following response: ", info);
        console.log("Logged in as: ", authorityType);
      }).catch(err => {
          console.log("Logging in from saved credentials failed, Resetting localstorage !!");
          localStorage.clear();
          console.log(err);
      })    
  }, []);


  const login = (pk, authorityType, entityInfo) => {
    if(loggedIn){
      console.log("Already logged in !");
      return false;
    }

    // Store private key locally for automatic login in future sessions
    localStorage.setItem('pk', pk);

    // Store authority type of the entity currently logged in
    localStorage.setItem('authorityType', authorityType);

    // Update login status in the context
    setEntityInfo(entityInfo);
    setAuthority(authorityType);
    setLoggedIn(true);
    console.log(localStorage.getItem('pk'));
    console.log(localStorage.getItem('authorityType'));
    console.log("Setup", pk, authorityType, entityInfo);
    return true;
  };


  const logout = () => {
    if(!loggedIn){
      console.log("Already logged out !");
      return false;
    }

    // Remove stored private key & address from local storage
    localStorage.removeItem('pk');
    localStorage.removeItem('address');
    localStorage.removeItem('authorityType');

    // Update login status in the context
    setWallet(undefined);
    setEntityInfo(undefined);
    setAuthority(undefined);
    setLoggedIn(false);

    return true;
  };


  const contextValue = {
    loggedIn,
    authority,
    entityInfo,
    wallet,
    login,
    logout
  };

  return <AuthContext.Provider value={contextValue} {...props} />;
};

const useAuth = () => React.useContext(AuthContext);

export { AuthProvider, useAuth };
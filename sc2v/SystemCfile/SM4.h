#include "systemc.h"

SC_MODULE(SM4){
    sc_in<sc_biguint<128> > key_in;
    sc_in<sc_biguint<128> > data_in;
    
    sc_out<sc_biguint<128> > data_out;
            
    void prc_SM4();
    
    SC_CTOR(SM4){
        SC_METHOD(prc_SM4);
        sensitive << key_in << data_in;
        dont_initialize();
    }
};

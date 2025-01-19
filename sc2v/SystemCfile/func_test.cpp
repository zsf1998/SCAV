#include "func_test.h"

void code_83::assign_out()
{
    out = function_code(din.read());

}
void code_83::assign_dout()
{
    dout = out.read();
}

sc_uint<3> code_83::function_code(sc_uint<8>  func_din)
{
    switch (func_din)
    {
    case 0b10000000:
    {
        func_code = 0x7;
        break;
    }
    case 0b01000000:
    {
        func_code = 0x6;
        break;
    }
    case 0b00100000:
    {
        func_code = 0x5;
        break;
    }
    case 0b00010000:
    {
        func_code = 0x4;
        break;
    }
    case 0b00001000:
    {
        func_code = 0x3;
        break;
    }
    case 0b00000100:
    {
        func_code = 0x2;
        break;
    }
    case 0b00000010:
    {
        func_code = 0x1;
        break;
    }
    case 0b00000000:
    {
        func_code = 0x0;
        break;
    }
    default:
    {
        
        func_code = 0x0;
        break;
    }
    }
    return func_code;
}






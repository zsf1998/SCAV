#include "code_83.hpp"

    
void code_83::assign_d_out()
{
	d_out = function_func_code(din);
}

void code_83::assign_dout()
{
	dout = d_out.read();
}


sc_uint<3> code_83::function_func_code(sc_uint<8> func_func_din)
{
switch(func_func_din)
{
    case 128:
            {
                func_code = 7;
                break;
            }
            case 64:
            {
                func_code = 6;
                break;
            }
            case 32:
            {
                func_code = 5;
                break;
            }
            case 16:
            {
                func_code = 4;
                break;
            }
            case 8:
            {
                func_code = 3;
                break;
            }
            case 4:
            {
                func_code = 2;
                break;
            }
            case 2:
            {
                func_code = 1;
                break;
            }
            case 0:
            {
                func_code = 0;
                break;
            }
            default:
            {
                func_code = 0;
            }
                break;
            }
            return func_code;
}

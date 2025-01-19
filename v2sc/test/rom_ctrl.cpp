#include "rom_ctrl.hpp"


void rom_ctrl::always_block1()
{
        if(sys_rst_n.read() == 0b0 )
        {
                cnt_200ms = 0b0;
        }
        else if(cnt_200ms.read() == CNT_MAX  || key1_en.read() == 0b1 || key2_en.read() == 0b1)
        {
                cnt_200ms = 0;
        }
        else
        {
                    cnt_200ms = cnt_200ms.read() + 0b1;
        }
    }

void rom_ctrl::always_block2()
{
        if(sys_rst_n.read() == 0b0 )
        {
                key1_en = 0b0;
        }
        else if(key2.read() == 0b1 )
        {
                key1_en = 0b0;
        }
        else if(key1.read() == 0b1 )
        {
            key1_en = ~key1_en.read();
        }
        else
        {
                ;
                key1_en = key1_en.read();
        }
    }

void rom_ctrl::always_block3()
{
        if(sys_rst_n.read() == 0b0 )
        {
                key2_en = 0b0;
        }
        else if(key1.read() == 0b1 )
        {
                key2_en = 0b0;
        }
        else if(key2.read() == 0b1 )
        {
            key2_en = ~key2_en.read();
        }
        else
        {
                ;
                key2_en = key2_en.read();
        }
    }

void rom_ctrl::always_block4()
{
        if(sys_rst_n.read() == 0b0 )
        {
                addr = 0;
        }
        else if(addr.read() == 5 && cnt_200ms.read() == CNT_MAX )
        {
                addr = 0;
        }
        else if(key1_en.read() == 0b1 )
        {
                addr = 99;
        }
        else if(key2_en.read() == 0b1 )
        {
                addr = 199;
        }
        else if(cnt_200ms.read() == CNT_MAX  )
        {
                addr = addr.read() + 0b1;
                        }
    }
}
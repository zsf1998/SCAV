#include "s_to_p.hpp"

void s_to_p::assign_ready_a()
{
    ready_a = 1;
}

void s_to_p::always_block1()
{
            if(!rst_n.read())
            {
                data_b = 0;
                data_b1 = 0;
            }
            else if(cnt.read() == 5 && valid_a.read() == 1)
            {
                data_b = data_b1.read();
            }
            else if(valid_a.read() == 1)
            {
                 data_b1 = (data_a.read(),data_b1.read().range(5,1));
            }
}

void s_to_p::always_block2()
{
            if(!rst_n.read())
            {
                cnt = 0;
            }
            else if(cnt.read() == 5)
            {
                cnt = 0;
            }
            else if(valid_a.read() == 1)
            {
                cnt = cnt.read() + 1;
            }
}

void s_to_p::always_block3()
{
            if(!rst_n.read())
            {
                valid_b = 0;
            }
            else if(cnt.read() == 5)
            {
                valid_b = 1;
            }
            else
            {
                valid_b = 0;
            }
}

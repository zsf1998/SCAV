#include "even_divide3.hpp"

void even_divide3::assign_clk3()
{
	clk3 = clk1.read() && clk2.read();
}

void even_divide3::always_block1()
{
        if(!rst.read() )
        {
                cnt = 0;
        }
        else if(cnt.read() == 2 )
        {
                cnt = 0;
        }
        else
        {
                    cnt = cnt.read() + 1;
        }
    }

void even_divide3::always_block2()
{
        if(!rst.read() )
        {
                clk1 = 0;
        }
        else if(cnt.read() == 1 )
        {
                clk1 = 0;
        }
        else if(cnt.read() == 2 )
        {
                clk1 = 1;
        }
    }

void even_divide3::always_block3()
{
        if(!rst.read() )
        {
                clk2 = 0;
        }
        else if(cnt.read() == 0 )
        {
                clk2 = 1;
        }
        else if(cnt.read() == 2 )
        {
                clk2 = 0;
        }
    }





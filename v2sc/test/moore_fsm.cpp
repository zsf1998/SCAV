#include "moore_fsm.hpp"


void moore_fsm::always_block1()
{
            if(!rst.read())
            {
                current_state = S0.read();
            }
            else
            {
                current_state = next_state.read();
            }
}

void moore_fsm::always_combilogic_block2()
{
        switch(current_state.read())
        {
        case S0:
              {
                  next_state = in.read() ? S1 : S0;
                  break;
              }
        case S1:
              {
                  next_state = in.read() ? S1 : S2;
                  break;
              }
        case S2:
              {
                  next_state = in.read() ? S3 : S0;
                  break;
              }
        case S3:
              {
                  next_state = in.read() ? S4 : S2;
                  break;
              }
        case S4:
              {
                  next_state = in.read() ? S1 : S0;
                  break;
              }
              default:
              {
                  next_state = S0.read();
                  break;
              }
}

void moore_fsm::always_block3()
{
            if(!rst.read())
            {
                out = 0;
            }
            else
            {
            switch(next_state.read())
            {
            case S0:
                  {
                      out = 0;
                      break;
                  }
            case S1:
                  {
                      out = 0;
                      break;
                  }
            case S2:
                  {
                      out = 0;
                      break;
                  }
            case S3:
                  {
                      out = 0;
                      break;
                  }
            case S4:
                  {
                      out = 1;
                      break;
                  }
                default:
                    break;
            }
            }
}

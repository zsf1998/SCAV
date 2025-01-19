#include "SM3_controller.hpp"


void SM3_Controller::assign_count_plus()
{
	count_plus = count.read() + 1;
}

    
void SM3_Controller::assign_ctrl()
{
	ctrl = next_state.read();
}


void SM3_Controller::always_block1()
{
            if(!rst.read())
            {
                current_state = idle.read();
            }
            else
            {
                current_state = next_state.read();
            }
}

void SM3_Controller::always_block2()
{
            if(!rst.read())
            {
                next_state = idle.read();
            }
            else
            {
            switch(current_state.read())
            {
            case idle:
                  {
                      if(W.read() == 0b1)
                      {
                          next_state = write.read();
                      }
                      else if(R.read() == 0b1)
                        {
                            next_state = read.read();
                        }
                        else
                        {
                            next_state = idle.read();
                        }
                      break;
                  }
            case write:
                  {
                      if(count.read() < 16)
                      {
                          next_state = write.read();
                      }
                      else
                      {
                          next_state = encryption.read();
                      }
                      break;
                  }
            case encryption:
                  {
                      if(count.read() < 69)
                      {
                          next_state = encryption.read();
                      }
                      else
                      {
                          if(R.read() == 0b1)
                          {
                              next_state = read.read();
                          }
                          else
                          {
                              next_state = idle.read();
                          }
                      }
                      break;
                  }
            case read:
                  {
                      next_state = idle.read();
                      break;
                  }
            }
}

void SM3_Controller::always_block3()
{
            if(!rst.read())
            {
                count = 0;
                finish = 0b0;
                count_out = 0;
            }
            else
            {
            switch(next_state.read())
            {
            case idle:
                  {
                      count_out = 0;
                      finish = 0b0;
                      count = 0;
                      break;
                  }
            case write:
                  {
                      finish = 0b0;
                      count = count_plus.read();
                      count_out = count_plus.read();
                      break;
                  }
            case encryption:
                  {
                      if(count_out.read() < 69)
                      {
                          finish = 0b0;
                          count = count_plus.read();
                          count_out = count_plus.read();
                      }
                      else
                      {
                          finish = 0b1;
                          count = count_plus.read();
                          count_out = 0;
                      }
                      break;
                  }
            case read:
                  {
                      finish = 0b0;
                      count_out = 0;
                      count = 0;
                      break;
                  }
            }
}

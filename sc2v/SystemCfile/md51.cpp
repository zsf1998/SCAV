//////////////////////////////////////////////////////////////////////
////                                                              ////
////  MD5 main implementation file                                ////
////                                                              ////
////  This file is part of the SystemC MD5                        ////
////                                                              ////
////  Description:                                                ////
////  MD5 main implementation file                                ////
////                                                              ////
////  To Do:                                                      ////
////   - done                                                     ////
////                                                              ////
////  Author(s):                                                  ////
////      - Javier Castillo, jcastillo@opencores.org              ////
////                                                              ////
//////////////////////////////////////////////////////////////////////
////                                                              ////
//// Copyright (C) 2000 Authors and OPENCORES.ORG                 ////
////                                                              ////
//// This source file may be used and distributed without         ////
//// restriction provided that this copyright statement is not    ////
//// removed from the file and that any derivative work contains  ////
//// the original copyright notice and the associated disclaimer. ////
////                                                              ////
//// This source file is free software; you can redistribute it   ////
//// and/or modify it under the terms of the GNU Lesser General   ////
//// Public License as published by the Free Software Foundation; ////
//// either version 2.1 of the License, or (at your option) any   ////
//// later version.                                               ////
////                                                              ////
//// This source is distributed in the hope that it will be       ////
//// useful, but WITHOUT ANY WARRANTY; without even the implied   ////
//// warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR      ////
//// PURPOSE.  See the GNU Lesser General Public License for more ////
//// details.                                                     ////
////                                                              ////
//// You should have received a copy of the GNU Lesser General    ////
//// Public License along with this source; if not, download it   ////
//// from http://www.opencores.org/lgpl.shtml                     ////
////                                                              ////
//////////////////////////////////////////////////////////////////////
//
// CVS Revision History
//
// $Log: not supported by cvs2svn $
// Revision 1.1.1.1  2004/10/08 14:04:10  jcastillo
// First import
//
// Revision 1.1.1.1  2004/09/08 16:24:49  jcastillo
// Initial release
//

//#include "md5.h"



void
md5::funcs ()
{
  sc_uint < 32 > aux, fr_var, tr_var, rotate1, rotate2;
  sc_uint < 8 > s_var;
  sc_uint < 4 > nblock;
  sc_uint < 32 > message_var[16];

  message_var[0]=message.read().range(511,480); 
  message_var[1]=message.read().range(479,448); 
  message_var[2]=message.read().range(447,416); 
  message_var[3]=message.read().range(415,384); 
  message_var[4]=message.read().range(383,352); 
  message_var[5]=message.read().range(351,320); 
  message_var[6]=message.read().range(319,288); 
  message_var[7]=message.read().range(287,256); 
  message_var[8]=message.read().range(255,224); 
  message_var[9]=message.read().range(223,192); 
  message_var[10]=message.read().range(191,160);  
  message_var[11]=message.read().range(159,128);  
  message_var[12]=message.read().range(127,96);  
  message_var[13]=message.read().range(95,64);  
  message_var[14]=message.read().range(63,32);  
  message_var[15]=message.read().range(31,0);   

  fr_var = 0;

  switch (round.read ())
    {
    case 0:
      fr_var = ((br.read () & cr.read ()) | (~br.read () & dr.read ()));
      break;
    case 1:
      fr_var = ((br.read () & dr.read ()) | (cr.read () & (~dr.read ())));
      break;
    case 2:
      fr_var = (br.read () ^ cr.read () ^ dr.read ());
      break;
    case 3:
      fr_var = (cr.read () ^ (br.read () | ~dr.read ()));
      fr_var = (cr.read () ^ br.read () | ~dr.read ());
      break;
    default:
      break;
    }

  tr_var = t.read ().range (43, 12);
  s_var = t.read ().range (11, 4);
  nblock = t.read ().range (3, 0);

  aux = (ar.read () + fr_var + message_var[(int) nblock] + tr_var);

  //cout << (int)round64.read() << " " << (int)fr_var << " " << (int)aux << " " << (int)nblock << " " << (int)message_var[(int)nblock] << endl;

  rotate1 = aux << (int) s_var;
  rotate2 = aux >> (int) (32 - s_var);
  func_out.write (br.read () + (rotate1 | rotate2));


	if (generate_hash.read () != 0)
	{
		next_ar.write (dr.read ());
		next_br.write (func_out.read ());
		next_cr.write (br.read ());
		next_dr.write (cr.read ());
	}


if (!reset)
    {
      ready_o.write (0);
      data_o.write (0);
      message.write (0);

      ar.write (0x67452301);
      br.write (0xEFCDAB89);
      cr.write (0x98BADCFE);
      dr.write (0x10325476);

      getdata_state.write (0);
      generate_hash.write (0);

      round.write (0);
      round64.write (0);

      A.write (0x67452301);
      B.write (0xEFCDAB89);
      C.write (0x98BADCFE);
      D.write (0x10325476);

    }

if (reset==0)
    {
      ready_o.write (0);


    }



    

}

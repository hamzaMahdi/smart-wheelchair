s = serial('/dev/cu.usbmodem14101','BAUD',115200)
 
fopen(s)
 
 while(1)
     out  = fscanf(s);
     C = strsplit(out,',');
     temp = cell2mat(C);
     initial = [0 0 0;0 0 0;0 0 0];
     
     output = find_position(temp,initial);
     
 end
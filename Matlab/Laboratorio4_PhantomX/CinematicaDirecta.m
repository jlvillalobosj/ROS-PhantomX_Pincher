%% Parámetros DH
clear;
clc;

% ws =   [-10 10 -10   10 -10 10];
ws = [-24 24 -24 24 -1 40];
L = [4.5, 10, 10, 1, 10]; 
offset = [0, -pi/2, 0, -pi/2, 0];

plot_options = {'workspace',ws,'scale',.5,'noa','view',[125 25], 'tilesize',2, ...
                'ortho', 'lightpos',[2 2 10], ...
                'floorlevel',0, 'base'};

%            Theta  d   a   alpha  type mdh offset  qlim
ParameterDH(1) = Link('revolute'   ,'alpha',      -pi/2,  'a',  0,      'd', ...
            L(1) , 'offset',    offset(1), 'qlim', [-0 2*pi]);

ParameterDH(2) = Link('revolute'   ,'alpha',      0,  'a',  L(2),      'd', ...
            0 , 'offset',    offset(2), 'qlim', [-pi/3 pi/3]);

ParameterDH(3) = Link('revolute'   ,'alpha',      0,  'a',  L(3),      'd', ...
            0 , 'offset',    offset(3), 'qlim', [-pi/2 pi/2]);

ParameterDH(4) = Link('revolute'   ,'alpha',      -pi/2,  'a',  0,      'd', ...
            0 , 'offset',    offset(4), 'qlim', [-2*pi/3 2*pi/3]);

ParameterDH(5) = Link('revolute'   ,'alpha',      0,  'a',  0,      'd', ...
            L(4)+L(5) , 'offset',    offset(5), 'qlim', [-2*pi/3 2*pi/3]);

Robot = SerialLink(ParameterDH,'name','Robot','plotopt',plot_options);

%% 

q = [90, 45, -55, 45, 20]*pi/180;
Robot.teach(q)
hold on
 xlim([-25 25])
 ylim([-25 25])
 zlim([-5 40])
 trplot(eye(4),'length',24);
%% TCP
Robot.tool = [ 1 0  0  0;...
              0 1  0  0;...
               0 0  1  0;...
               0 0  0  1];
Robot = SerialLink(ParameterDH,'name','Robot','plotopt',plot_options)
%% Teach robot
q = [0 0 0 0 0];
Robot.teach(q)
hold on
trplot(eye(4),'length',24);
%% Pinta los sistemas de coordenadas
M = Robot.base;
for i=1:Robot.n
    M = M * ParameterDH(i).A(q(i));
    trplot(M,'rgb','frame',num2str(i),'length',3)
end
%%  Cinematica Directa.
TCP = Robot.fkine(q)
trplot(TCP,'length',2 )
tr2rpy(TCP,'zyx','deg')
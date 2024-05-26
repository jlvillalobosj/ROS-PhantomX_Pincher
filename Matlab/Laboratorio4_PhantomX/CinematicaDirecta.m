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
            L(1) , 'offset',    offset(1), 'qlim', [-pi pi]);

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

q = [0, 0, 0, 0, 0]*pi/180;
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
q = [ 0 0 0 0 0];
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
MTH01=transforma(0, 4.5, 0, -90);
MTH12=transforma(-90, 0, 10, 0);
MTH23=transforma(0, 0, 10, 0);
MTH34=transforma(-90, 0, 0, -90);
MTH45=transforma(0,11, 0, 0);
MTH_tcp =MTH01*MTH12*MTH23*MTH34*MTH45;

TH01=DH(0, 4.5, 0, -90);
TH12=DH(-90, 0, 10, 0);
TH23=DH(0, 0, 10, 0);
TH34=DH(-90, 0, 0, -90);
TH45=DH(0,11, 0, 0);
TH_tcp =TH01*TH12*TH23*TH34*TH45;

TCP = Robot.fkine(q)
trplot(TCP,'length',2 )
tr2rpy(TCP,'zyx','deg')

function M = DH(theta,d,a,alpha)
 Rz = [rotz(theta) zeros(3,1);zeros(1,3) 1];
 Rx = [rotx(alpha) zeros(3,1);zeros(1,3) 1];
 M = Rz*transl(a,0,d)*Rx;
end

function MTH = transforma(th,d,a,alpha)
 M1=[cosd(th) -sind(th)*cosd(alpha) sind(th)*sind(alpha) a*cosd(th)];
 M2=[sind(th) cosd(th)*cosd(alpha) -sind(alpha)*cosd(th) sind(th)*a];
 M3=[0 sind(alpha) cosd(alpha) d];
 MTH=[M1;M2;M3;0 0 0 1];
end

function [drms, dr, cr2, nx2, nt, w2, w2x, d, w1] = fullcomp()
%
% INPUT
%
%
%
% OUTPUT
%
% drms         RMS of original image
% dr           Dynamic range (log_10(dr) is the n.significant decimal digits)
%              Given by max(|d|)/drms
% cr2          ratio of compressed v. uncompressed data size.
% nx2          Number of bits of compressed data
% nt           Number of bits of uncompressed data
% w2           Approximated image
% w2x          Image loaded from compressed data file (sanity check).
% d            The original image

%
% Read the required values
%
disp (' ')
disp('Enter the required data')
fnamer = input(['\nEnter the ROOT NAME of the FITS file: \n', ...
               '       e.g. for aa.fits enter ''a'' ==>  ']);
ng = input('\nEnter the number of Guard digits, (G in the paper). \n', ...
               '       Recommended 0 or 1 ==>  ');
check = input(['\nEnter =/= 0 to load the compressed file and generate an image (w2x)\n', ...
               '       == 0 to skip it\n',...
               '       Enter choice ==>  ']);

%
% 1. Read the image from the FITS file
%
d = fitsread([fnamer,'.fits']);
disp('  ')
disp ('1. FITS file read and scaled')

%
% 2. Scale the image as required
%
[dx,drms,dr,nb,f1,nx,nt,cr,sc,w1,w2,q1] = scaleimage(fnamer,ng,d);
disp ('2. FITS files writtten: compressed and difference')

%
% 3. write the compressed image to output file
%
[nx2, cr2, fname] = puttogether3(fnamer,nb,sc,w1,q1);
disp ('3. The compressed file is written')

%
% 4. Read the compressed file to check that all s right
%
if (check~=0)
    [w2x] = getimage(fname);
    disp ('4. the compressed file is read and an image is produced for sanity check')
else
    w2x = [];
end

namemat = [fnamer,'.mat'];
% save namemat fnamer drms dr ng nx2 nt cr2 d nb sc w1 w2 w2x
save (namemat,'fnamer', 'drms', 'dr', 'ng', 'nx2', 'nt', 'cr2', 'nb', 'sc', ...
    'd', 'w1', 'w2', 'w2x');
disp '5. Matlab .mat file saved'

end

%
%===================================================================
%===================================================================
%

function [dx,drms,dr,nb,f1, nx, nt, cr, sc, w1, w2, q1] = scaleimage(fnamer,ng,d)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

n = size(d,1);

nn = 32;
m = size(d,1);
n = size(d,2);

dx = max(max(abs(d)));
nb=32;
drms = getrms(nb,d);

% drms = 0.03;
dr = dx/drms;
if (dx<1)
    nb = fix(1+log2(dx/drms)-log2(dx))+ng;
%     nb = fix(1+log2(dx/drms))+fix(1-log2(dx))+ng;
else
    nb = fix(1+log2(dx/drms)-log2(dx))+ng;
end
f1 = 2^nb;

w1 = round(f1*d); sc = -min(min(w1)); w1 = w1+sc; w2 = (w1-sc)/f1;

q1 = uint32(w1); q1(w1>0) = uint32(fix(1+log2(w1(w1>0))));
w1 = uint32(w1);


n3 = sum(sum(q1));
n2 = numel(q1);
nl = fix(0.99999+log2(single(max(max(q1)))));
nx = n3+nl*n2;
nt = 32*numel(d);
cr = nx/nt;

% [w1x, dq] = puttogether(q1,w1);

fitswrite(single(d),[fnamer, '_orig.fits']);
fitswrite(single(w2),[fnamer, '_comp.fits']);
fitswrite(single(w2-d),[fnamer, '_diff.fits']);

end

%
%===================================================================
%===================================================================
%

function [nx2, cr2, fname] = puttogether3(fnamer, nb, sc, w1, q1)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

m = size(q1,1);
n = size(q1,2);
n2 = numel(q1);

ndl = int32(fix(1+log2(single(max(max(q1))))));
z = blanks(32);
k1 = 0;
k2 = 0;
nu = 32;
ni = 16;
nk1 = nu*ni;
nkk = nk1+nu;

m1 = sum(sum(q1));
m2 = n2;
m2 = ndl*m2;

ndq = fix(single(nu-1+sum(sum(q1))+ndl*n2)/nu);
dq = zeros(1,ndq,'uint32');

z = blanks(nkk);
z(1:end) = '0';

idq = 0;
for j = 1:n
    for i=1:m
        k1 = k2+1;
        k2 = k2+ndl;
        nq = q1(i,j);
        z(k1:k2) = dec2bin(nq,ndl);
        if (nq ~= 0)
            k1 = k2+1;
            k2 = k2+int32(nq);
            z(k1:k2) = dec2bin(w1(i,j),nq);
        end
        if (k2>nk1)
            for ll=1:nu:nk1
                idq = idq+1;
                dq(idq) = bin2dec(z(ll:ll+nu-1));;
            end
            nk = k2-nk1;
            if (nk>0)
                z(1:nk) = z(nk1+1:nk1+nk);
            end
            z(nk+1:nkk) = '0';
            k2 = nk;
        end
    end
end


if (k2>0)
    z(k2+1:nkk) = '0';
    for ll=1:nu:k2
        idq = idq+1;
        dq(idq) = bin2dec(z(ll:(ll+31)));
    end
end
nx2 = nu*numel(dq);
cr2 = nx2/(32*n2);

fname = [fnamer,'_comp.dat'];
fid = fopen(fname,'w');
count = fwrite(fid,int64(m),'int64');
count = fwrite(fid,int64(n),'int64');
count = fwrite(fid,int32(nb),'int32');
count = fwrite(fid,int32(sc),'int32');
count = fwrite(fid,int32(ndl),'int32');
count = fwrite(fid,int64(ndq),'int64');
count = fwrite(fid,dq,'uint32');
fclose(fid);

w116 = uint32(w1);
fnamex = [fnamer,'_uint16.dat'];
fid = fopen(fnamex,'w');
count = fwrite(fid,int64(m),'int64');
count = fwrite(fid,int64(n),'int64');
count = fwrite(fid,int32(nb),'int32');
count = fwrite(fid,int32(sc),'int32');
count = fwrite(fid,int32(ndl),'int32');
count = fwrite(fid,int64(ndq),'int64');
count = fwrite(fid,w116,'uint32');
fclose(fid);

end

%
%===================================================================
%===================================================================
%

function [w2] = getimage(fname)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

fid = fopen(fname,'r');
m = int64(fread(fid,1,'int64'));
n = int64(fread(fid,1,'int64'));
nb = int32(fread(fid,1,'int32'));
sc = int32(fread(fid,1,'int32'));
ndl = int32(fread(fid,1,'int32'));
ndq = int64(fread(fid,1,'int64'));
dq = uint32(fread(fid,ndq,'uint32'));
fclose(fid);

f1 = single(2^nb);

n2 = m*n;
w1 = zeros(n,n,'uint32');
w2 = zeros(n,n,'single');

k1 = 0;
k2 = 0;
nu = 32;
ni = 32;
nk1 = nu*ni;
nkk = nk1+ni;

% z = blanks(nkk);
% z(1:end) = '0';

z='';
for i=1:ndq
z(nu*(i-1)+1:i*nu) = dec2bin(dq(i),nu);
end

k2 = 0;
for j=1:n
    for i=1:m
        k1 = k2+1;
        k2 = k2+ndl;
        nl = bin2dec(z(k1:k2));
        if (nl>0)
            k1 = k2+1;
            k2 = k2+nl;
            w1(i,j) = bin2dec(z(k1:k2));
        end
    end
end

w2 = (single(w1)-single(sc))/f1;

end

%
%===================================================================
%===================================================================
%

function [rmsx] = getrms(nb,d)
%UNTITLED6 Summary of this function goes here
%   Detailed explanation goes here

m = size(d,1);
n = size(d,2);

mnb = fix((m+nb-1)/nb);
nnb = fix((m+nb-1)/nb);

for j=1:mnb
    j1 = (j-1)*nb+1;
    j2 = min(j*nb,m);
    for i=1:nnb
        i1 = (i-1)*nb+1;
        i2 = min(i*nb,n);
        z = d(i1:i2,j1:j2);
        r(i,j) = rms(z(1:numel(z)));
    end
end

rmsx = min(min(r));

end




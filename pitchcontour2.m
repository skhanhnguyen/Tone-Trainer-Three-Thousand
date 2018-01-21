function res = pitchcontour2(args)
data = args.arg1;
data = data(:,1);
fs=16000
% Apply window
data = data.*chebwin(length(data));
active = find(abs(data) >= 0.05);
data = data(active(1):active(end));
data = data(1:(floor(length(data)/100)*100));
T = 1/fs;
L = length(data);
t = (0:L-1)*T;
duration = T*(L-1);


subsize = 10;
redata = reshape(data, length(data)/subsize, subsize);
freq = [];
for i=(1:subsize)
    Y = fft(redata(:,i));
    L = length(redata(:,i));
    P2 = abs(Y/L);
    P1 = P2(1:L/2+1);

    P1(2:end-1) = 2*P1(2:end-1);
    f = fs*(0:(L/2))/L;
%         figure
%         plot(f,P1)
    peaks = find(P1 > mean(P1)+2*var(P1)^0.5);
    fund_freq = f(peaks(1));
    if fund_freq > 500
        freq = [];
        break
    end
    freq = [freq fund_freq];
end
%     freq = freq./max(freq);
y = [freq [freq(2:subsize)-freq(1:subsize-1)] freq(subsize)-freq(1) duration];
res = y;
end
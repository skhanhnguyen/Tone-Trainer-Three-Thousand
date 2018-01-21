function ans = pitchcontour_function(args)
fs = 16000;
data = args.arg1;
data = data(:,1);
% Apply window
%     data = data.*chebwin(length(data));
active = find(abs(data) >= 0.1);
data = data(active(1):active(end));
data = data(1:(floor(length(data)/100)*100));
T = 1/fs;
L = length(data);
t = (0:L-1)*T;

%     
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
    if fund_freq > 1000
        freq = [];
        break
    end
    freq = [freq fund_freq];
    
    ans = freq
end
end
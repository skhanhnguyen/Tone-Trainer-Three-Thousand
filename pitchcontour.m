directory = dir();
%1: 3:327
%2: 328:651
%
%4: 976:1299
y = []
for file=(3:27)
%     if file==3 || file==328 || file==652 || file==976
%         figure
%     end
    filename = directory(file).name;
    [data, fs] = audioread(filename);
    data = data(:,1);
    % Apply window
%     data = data.*chebwin(length(data));
    active = find(abs(data) >= 0.1);
    data = data(active(1):active(end));
    data = data(1:(floor(length(data)/100)*100));
    T = 1/fs;
    L = length(data);
    t = (0:L-1)*T;
    

    subplot(1,2,1)
    plot(t,data)
    title(filename)
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
    end
%     freq = freq./max(freq);
    subplot(1,2,2)
    if not(isempty(freq))
        plot(freq)
        y = [y; str2num(filename(1)) freq];
    end
    axis([0 10 0 2000])
    hold on
    title(filename);
end
hold off
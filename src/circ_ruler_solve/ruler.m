clear all;
clc;

N = 43;
n_rows = 0;
for distance=1:N-2,
    for start=1:N-distance,
        stop = mod(start+distance-1,N)+1;
        if stop < start,
            continue
        end
        n_rows = n_rows + 1;
    end
end

A = zeros(n_rows, n_rows + N);
Aeq = zeros(N, N + n_rows);
beq = ones(N, 1);

row_num = 1;
for distance=1:N-2,
    for start=1:N-distance
        stop = mod(start+distance-1,N)+1;

        if stop < start,
            continue
        end
        A(row_num, start) = -1;
        A(row_num, stop) = -1;
        A(row_num, N + row_num) = 2;
        Aeq(distance, row_num + N) = 1;
        row_num = row_num + 1;
    end
end

Aeq(N - 1, 1) = 1;
Aeq(N, N) = 1;


f = [ones(N, 1); zeros(row_num - 1, 1)];

lb = zeros(n_rows + N, 1);
ub = ones(n_rows + N, 1);
b = zeros(n_rows, 1);
intcon = 1:1:(n_rows + N);

x = intlinprog(f,intcon,A,b,Aeq,beq,lb,ub)
r = round(x(1:N)')
sum(r)

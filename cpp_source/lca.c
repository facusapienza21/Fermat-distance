#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

#define dbgon

#ifdef dbgon
    #define dbgar(xs, n) printf(#xs); for(size_t i = 0; i < n; i++) printf(" %d", xs[i]); printf("\n");
    #define dbgi(n) printf(#n); printf(" es %d\n", n);
    #define dbgd(n) printf(#n); printf(" es %f\n", n);
#else
    #define dbgar(xs, n)
    #define dbgi(n)
    #define dbgd(n)
#endif

typedef struct struct_rmq {
    double *table;
    int n;
    int logn;
} RMQ;

typedef struct struct_lca
{
    int *prev;
    int *et;
    int n;
    int root;
    double *distances;
    int *right;
    RMQ rmq;
} lca;

double min(double a, double b){
    return a < b ? a : b;
}

double query_rmq(RMQ rmq, int from, int to){
    to++;
    int p = 31-__builtin_clz(to-from);
    return min(rmq.table[p*rmq.n+from], rmq.table[p*rmq.n + to - (1<<p)]);
}

RMQ create_rmq(double* values, int n){
    int logn = 31-__builtin_clz(n);
    double *table = (double*) malloc (n * (logn+1) * sizeof(double));
    memcpy(table, values, n*sizeof(double));    

    for(int p = 0; p < logn; p++)
    {
        for(int x = 0; x < n-(1<<p); x++)
        {
            table[(p+1)*n + x] = min(table[p*n + x], table[p*n+x+(1<<p)]);
        }
        for(int x = n-(1<<p); x < n; x++)
        {
            table[(p+1)*n + x] = table[p*n + x];
        }
    }
    RMQ res;
    res.table = table;
    res.n = n;
    res.logn = logn;
    return res;
}

int *get_right(int *et, int n){

    int *res = (int*) malloc (n * sizeof(int));
    
    for(int i = 0; i < 2*n-1; i++)
    {
        res[et[i]] = i;
    }

    return res;
}

void do_euler_tour(int current, int *i, int *res, int *children, int *next_sibling){
    
    int child = children[current];
    res[*i] = current;
    ++*i;
    while(child != -1)
    {
        do_euler_tour(child, i, res, children, next_sibling);
        child = next_sibling[child];
        res[*i] = current;
        ++*i;
    }
}

int* euler_tour(int n, int *prev, int root){

    int* children = (int*) malloc(n * sizeof(int));
    memset(children, -1, n * sizeof(int));
    
    int* next_sibling = (int*) malloc(n * sizeof(int));
    memset(next_sibling, -1, n * sizeof(int));
    
    for(int child = 0; child < n; child++)
    {
        if (child != root && prev[child] >= 0)
        {
            int parent = prev[child];
            next_sibling[child] = children[parent];
            children[parent] = child;
        }
    }

    int i = 0;
    int* res = (int*) malloc((2*n-1) * sizeof(int)); 

    do_euler_tour(root, &i, res, children, next_sibling);

    free(children);
    free(next_sibling);

    return res;
}

double get_lca_distance(lca tree, int a, int b){
    if (a == b)
        return tree.distances[a];    
    int ra = tree.right[a];
    int rb = tree.right[b];
    if (ra > rb){
        ra = rb;
        rb = tree.right[a];
    }
    return query_rmq(tree.rmq, ra, rb);
}

double *map_index_to_values(int *index, double *values, int index_size){
    double *res = (double*) malloc(index_size * sizeof(double));
    for(int i = 0; i < index_size; i++)
    {
        res[i] = values[index[i]];
    }
    return res;
}

double get_distance(lca tree, int a, int b){
    double res = tree.distances[a] + tree.distances[b] - 2*get_lca_distance(tree, a, b);
    return res;
}

lca create_lca(int root, int *prev, int n, double *distances)
{
    lca tree;
    tree.root = root;
    tree.n = n;
    // tree.prev = prev;
    tree.prev = (int*) malloc(n * sizeof(int));
    memcpy(tree.prev, prev, n * sizeof(int));
    
    // tree.distances = distances;
    tree.distances = (double*) malloc(n * sizeof(double));
    memcpy(tree.distances, distances, n * sizeof(double));

    tree.et = euler_tour(n, prev, root);
    tree.right = get_right(tree.et, n);

    double *distances_on_et = map_index_to_values(tree.et, distances, 2*n-1);
    tree.rmq = create_rmq(distances_on_et, 2*n-1);
    free(distances_on_et);

    return tree;
}

void free_rmq(RMQ rmq){
    free(rmq.table);
}

void free_lca(lca tree)
{
    free(tree.prev);
    free(tree.distances);
    free(tree.et);
    free(tree.right);
    free_rmq(tree.rmq);
}

void get_distances(lca tree, double* res){
    for(size_t i = 0; i < tree.n; i++)
    {
        res[i*tree.n + i] = 0;
        for(size_t j = 0; j < i; j++)
        {
            res[i*tree.n + j] = res[j*tree.n + i] = get_distance(tree, i, j);
        }
    }
}
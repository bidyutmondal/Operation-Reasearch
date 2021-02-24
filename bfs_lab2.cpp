#include <cstdio>
#include <iostream>

using namespace std;

double gauss_elimination(double a[][100], int m,int n, int store_2d_arr[], double objective[])
{
    int i,j,k,l,key,flag,track=0;
    double er=0.001,val,x[100],x0[100],sum,a_new[100][100],c;
    for(i=0;i<m;i++)
        x[i] = 0.0;
    for(j=0; j<m; j++) {
        for(i=0; i<m; i++) {
            if(i>j){
                c=a[i][j]/a[j][j];
                for(l=0; l<m+1; l++) {
                    a[i][l]=a[i][l]-c*a[j][l];
                }
            }
        }
    }
    x[m-1]=a[m-1][m]/a[m-1][m-1];
    for(i=m-1; i>=0; i--) {
        sum=0;
        for(j=i+1; j<m; j++) {
            sum=sum+a[i][j]*x[j];
        }
        x[i]=(a[i][m]-sum)/a[i][i];
    }
    int check_infeasibility = 0,check_degeneracy = 0;
    double obj_val=0.0;
    
    for(i=0,j=0;i<n;i++) {
        flag = 0;
        for(k=0;k<(n-m);k++)  {
            if(store_2d_arr[k] == i) 
                    flag = 1;
        }
        if (flag==0) {   
            if (x[j] < 0) {
                check_infeasibility = 1;
            }
            else {
                obj_val += (objective[i]*x[j]);
            }
            printf(" x%d = %lf ",i+1,x[j++]);
        }
    }
    for(i=0;i<(n-m);i++) {
        for(j=i+1;j<(n-m);j++) {
            if(x[i] == x[j] && x[i] > 0) {
                check_degeneracy = 1;
            }
        }
    }
    if(check_degeneracy==1) {
        printf(" - Degenerate solution");
    }
    if(check_infeasibility==0 && check_degeneracy==0)  {
        printf(" - Basic feasible solution");
    }
    if(check_infeasibility==1) {
        obj_val = 0.0;
        printf(" - Infeasible solution\n");
    }
    else {
        printf(" - Desired Objective function value = %lf\n",obj_val);
    }
    return obj_val;
}


int number_combine(int arr[], int store_Data[], int start, int end,int index, int r, int s)
{
    int i;
    if (index == r)
        return(s+1);
    
 
    for (i=start; i<=end && end-i+1 >= r-index; i++) {
        store_Data[index] = arr[i];
        s = number_combine(arr, store_Data, i+1, end, index+1, r, s);    
    }
    return s;
}


int * combine(int arr[], int store_Data[], int start, int end,int index, int r, int* store_arr, int *l)
{
    int j,i;
    if (index == r) {
        for (j=0; j<r; j++) {
            *(store_arr + *l) = store_Data[j];
            (*l)++;
        }
        return store_arr;
    }
 
    for (i=start; i<=end && end-i+1 >= r-index; i++) {
        store_Data[index] = arr[i];
        store_arr = combine(arr, store_Data, i+1, end, index+1, r, store_arr, l);    
    }
    return store_arr;
}


int main() {
    int i,j,m,n,optimal;
    printf("\n Enter number of unknowns Including slack variables[No. of inequality equations] (n) : ");
    scanf("%d",&n);
    printf(" Enter number of equations (m) : ");
    scanf("%d",&m);
    double a[m][n],b[m],objective_function[n];
    printf("\nGive Input :\n");
    cout << "Matrix A=>\n";
    for(i=0;i<m;i++)  {
        for(j=0;j<n;j++){
            printf(" row %d column %d : ",(i+1),(j+1));
            scanf("%lf",&a[i][j]);
        }
    }
    printf("\nMatrix B =>\n");
    for(i=0;i<m;i++) {
        printf(" row %d column 1 : ",(i+1));
        scanf("%lf",&b[i]);
    }
    printf("\n");
    for(i=0;i<n;i++) {
        printf(" Input for objective function's coefficient of x%d : ",(i+1));
        scanf("%lf",&objective_function[i]);
    }
    printf(" \n\n 1 : Maximize \n 2 : Minimize \n Enter optimization technique for objective function (1 or 2) : ");
    scanf("%d",&optimal);
    int arr[n],k;
    for(i=0;i<n;i++) 
        arr[i] = i;
    int r = n-m;
    int store_Data[r];
    int nc = number_combine(arr, store_Data, 0, n-1, 0, r,0);
    int *getarr;
    int store_arr[nc*r+1];
    int store_2d_arr[nc+1][r+1];
    getarr = store_arr;
    int l_start = 0;
    int *l = &l_start;
    getarr = combine(arr, store_Data, 0, n-1, 0, r, getarr, l);
    for (i=0;i<nc;i++) {
        for(j=0;j<r;j++) {
            store_2d_arr[i][j] = store_arr[i*r+j];
        }
    }

    double a_new[100][100],sum[nc],replace;
    int flag, track, h;

    for(i=0;i<nc;i++){
        printf("\n");
        cout << "=>   ";
        for(j=0;j<r;j++) {
            printf(" x%d = 0.000000 ",store_2d_arr[i][j]+1);
        }
        track = 0;
        for(j=0;j<n;j++) {
            flag = 0;
            for(k=0;k<(n-m);k++){
                if(store_2d_arr[i][k] == j) {
                        flag = 1;
                    }
            }
            if (flag==0)  {
                for(h=0;h<m;h++) {
                    a_new[h][j-track] = a[h][j];                
                }
            }
            else {
                track = track+1;
            }
        }
        for(h=0;h<m;h++) {
            a_new[h][m] = b[h];
        }
        sum[i] = gauss_elimination(a_new,m,n,store_2d_arr[i],objective_function);
    }

    if(optimal==1) {
        for (i = 0; i < nc; ++i) {
            for (j = i + 1; j < nc; ++j) {
                if (sum[i] < sum[j]) {
                    replace =  sum[i];
                    sum[i] = sum[j];
                    sum[j] = replace;
                }
            }
        }
    }
    else {
        for (i = 0; i < nc; ++i) {
            for (j = i + 1; j < nc; ++j)  {
                if (sum[i] > sum[j])  {
                    replace =  sum[i];
                    sum[i] = sum[j];
                    sum[j] = replace;
                }
            }
        }               
    }

    if(sum[0]==sum[1]) {
        if(sum[0] == 0) {
            printf("\n\n There is No optimal solution.");
        }
        else {
            printf("\n\n Infinitely many optimal solutions, with optimal objective function value = %lf",sum[0]);
        }
    }
    else {
        printf("\n\n Exactly one optimal solution, with optimal objective function value = %lf",sum[0]);        
    }
    printf("\n");
}

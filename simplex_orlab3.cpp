//Bidyut Mondal
//18MA20010

#include <bits/stdc++.h>
using namespace std;

void calculate(vector<string>cs, int iter, int extra_var, int total_var, vector<double>& c, vector<double>& z, vector<double>& diff, vector<double>& cb, vector<vector<double> > A);

void calc_pivot(int iter,vector<string>cbs, int extra_var, int total_var, vector<double>& c, vector<double>& z, vector<double>& diff, vector<double>& cb, vector<vector<double> > A, vector<double>& d, int *pivcol, int *pivrnum);

void table_gen(int iter, int extra_var, int total_var, vector<vector<double> >&A, vector<double> &d, int pivrnum, int pivcol);
//Question1
//Write code to express any LPP in standard form as above using slack/surplus variables.
//Reduce the LPP in the standard form
int main(){
	//Number of unknowns
	int n;
	cout<<"Enter the number of unknowns \n";
	cin>>n;
    cout<<"Enter 1 for Maximization and 2 for Minimization \n";
    int max_min;
    cin>>max_min;
	vector<double> coeff;
	cout<<"Enter coefficients of the optimisation equation  \n";
	for(int i=0;i<n;i++)
	{
		double x;
		cin>>x;
        if(max_min==2) x *= -1;
		coeff.push_back(x);
	}
    double d_opt;
    cout<<"Enter constant of the optimisation equation  \n";
    cin>>d_opt;
	//Number of inequations
	int m;
	cout<<"Enter the number of inequation  \n";
	cin>>m;
	//For constants in the inequality
	vector<double> d;
	//int coeffineq[m][n];
	vector<vector<double> > coeffineq;
	//Count slack and surplus variable
	int slack_var=0;
	int surplus_var=0;
	for(int i=0;i<m;i++)
	{
		int choice;
		cout<<"Enter 1 for <= type or 2 for >= inequality \n";
		cin>>choice;
		cout<<"Enter coefficient of eqn no."<<i+1<<endl;
		vector<double>temp;
		for(int j=0;j<n;j++)
		{
			double x;
			cin>>x;
			if(choice==1)
				temp.push_back(x);
			else
				temp.push_back(x*(-1.0));
		}
		coeffineq.push_back(temp);
		temp.clear();
		cout<<"Enter value of eqn no."<<i+1<<"\n";
		double x1;
		cin>>x1;
		if(choice==1)
			d.push_back(x1);
		else
			d.push_back(x1*(-1.0));
		slack_var++;
	}

	//Construction of reduced LPP
	cout<<"LPP in standard form \n";
	for(int i=0;i<n;i++)
	{
		cout<<"+ "<<coeff[i]<<"*"<<"x"<<i+1;
	}
	//S1 for slack variables
	//A for artificial
	for(int i=0;i<slack_var;i++)
	{
		cout<<"+ "<<"0*x"<<n+i+1;
	}
	cout<<"\n";

	//Q2
	//Write code to print
	//• a(j) = col(a1j ; a2j ; :::; amj)
	//• A = [a(1); a(2); :::; a(j); :::a(n)]
	//• B = (b(1); b(2); :::; b(m)), which is basis matrix.
	//• Basic solution xB = B􀀀1b = col(xBi ; i = 1; 2; :::;m)
	//• cB = col(cB1 ; cB2 ; :::; cBm), cBi being the coecient of basic variable xBi ; i = 1; 2; :::;m in the objective function.
	//• y(j) = col(y1j ; y2j ; :::; yij ; :::; ymj) = B􀀀1a(j); j = 1; 2; :::; n2
	//• z(xB) = cTBxB and zj = cT By(j); j = 1; 2; :::; n
	int extra_var=slack_var+surplus_var;
	int total_var=n+extra_var;
	vector<vector<int> > B;
	for(int i=0;i<extra_var;i++)
	{
		vector<int>tempB;
		for(int j=0;j<extra_var;j++)
		{
			if(i==j)
				tempB.push_back(1);
			else
				tempB.push_back(0);
		}
		B.push_back(tempB);
		tempB.clear();
	}
	cout<<"Basis Matrix \n";
	for(int i=0;i<extra_var;i++)
	{
		for(int j=0;j<extra_var;j++)
		{
			cout<<B[i][j]<<" ";
		}
		cout<<"\n";
	}
	cout<<"\n";

	//Matrix A extra_var*total_var
	vector<vector<double> > A;
	for(int i=0;i<extra_var;i++)
	{
		vector<double>tempA;
		for(int j=0;j<total_var;j++)
		{
			if(j<n)
				tempA.push_back(coeffineq[i][j]);
			else
			{
				if((j-n)==i)
					tempA.push_back(1);
				else
					tempA.push_back(0);
			}
		}
		A.push_back(tempA);
		tempA.clear();
	}
	cout<<"Input matrix A \n";
	for(int i=0;i<extra_var;i++)
	{
		for(int j=0;j<total_var;j++)
		{
			cout<<A[i][j]<<" ";
		}
		cout<<"\n";
	}
	cout<<"\n";

	//Display all column vectors
	cout<<"Column vectors a1, a2,.........\n";
	for(int i=0;i<total_var;i++)
	{
		cout<<"Column vector a"<<i+1<< "  \n";
		for(int j=0;j<m;j++)
		{
			cout<<A[j][i]<<" ";
		}
		cout<<"\n";
	}

	//Display cb coefficient of basic variable in objective function
	cout<<"Coefficient of basic variable in objective function \n";
	//int cb[extra_var];
	vector<double>cb;
	for(int i=0;i<extra_var;i++)
	{
		cb.push_back(0.0);
	}
	for(int i=0;i<extra_var;i++)
	{
		cout<<cb[i]<<" ";
	}
	cout<<"\n";

	//Q3 Finding cj and zj
	//Finding cj values
	//int c[total_var];
	vector<double>c;
	cout<<"\n";
	cout<<"Values of cj \n";
	for(int i=0;i<n;i++)
	{
		c.push_back(coeff[i]);
	}
	for(int i=0;i<extra_var;i++)
	{
		c.push_back(cb[i]);
	}
	for(int i=0;i<total_var;i++)
	{
		cout<<c[i]<<" ";
	}
	cout<<"\n";
	//Finding zj
	vector<string>cs;
	vector<string>cbs;
	for(int i=0;i<total_var;i++)
	{
		if(i==0)
			cs.push_back("x1");
		else if(i==1)
			cs.push_back("x2");
		else if(i==2)
			cs.push_back("x3");
		else if(i==3)
			cs.push_back("x4");
		else if(i==4)
			cs.push_back("x5");
		else if(i==5)
			cs.push_back("x6");
		else if(i==6)
			cs.push_back("x7");
		else if(i==7)
			cs.push_back("x8");
		else if(i==8)
			cs.push_back("x9");
		else
			cs.push_back("x10");
	}
	for(int i=n;i<total_var;i++)
	{
		cbs.push_back(cs[i]);
	}

	cout<<"\n";
	vector<double>z;
	for(int i=0;i<total_var;i++)
		z.push_back(0.0);
	vector<double>diff;
	////////////////////
	int iter=0;
	cout<<"Iteration 0 starts \n";

	calculate(cs, iter, extra_var, total_var, c, z, diff,cb,A);
	//Q4
	//Finding pivot row, pivot column, pivot element, minimum ratio

	int pivrnum=0;
	int pivcol=0;
	calc_pivot(iter, cbs, extra_var, total_var, c, z, diff,cb,A, d, &pivcol, &pivrnum);
	//To check if solution is reached
	//while loop to iterate till solution is found
	iter++;
	while(1)
	{
		//Update value of A d and cb
		table_gen(iter, extra_var, total_var, A, d, pivrnum, pivcol);
		//Update coefficient of basic variable
		cb[pivcol]=c[pivrnum];
		cbs[pivcol]=cs[pivrnum];
		z.clear();
		diff.clear();
		for(int i=0;i<total_var;i++)
			z.push_back(0.0);
		calculate(cs, iter, extra_var, total_var, c, z, diff,cb,A);
		calc_pivot(iter, cbs, extra_var, total_var, c, z, diff,cb,A, d, &pivcol, &pivrnum);
		//Check if solution is terminated
		int flag=0;
		for(int i=0;i<total_var;i++)
		{
			if(diff[i]<0.0)
			{
				flag=1;
				break;
			}
		}
		if(flag==0)
		{
			cout<<"No. of iterations needed "<<iter<<"\n";
			cout<<"Values of the basic variables are \n";
			for(int i=0;i<extra_var;i++)
			{
				cout<<cbs[i]<<" = "<<d[i]<<"\n";
			}
			//Find the value of the objective function
			double res=0.0;
			for(int i=0;i<extra_var;i++)
			{
				res+=(cb[i]*d[i]);
			}
			cout<<"\n";
            if(max_min == 2) res *= -1;
			cout<<"Optimal value of the function is "<<res+d_opt<<"\n";
			//Check if infinite solution exist
			//in infinite the Zj-Cj value corresponding to any varia
			return 0;
		}
		else
		{
			//Check if we have unbounded situation 
			//In unbounded situation pivot column has all non positive elements
			int fl=0;
			for(int i1=0;i1<extra_var;i1++)
			{
				if(A[i1][pivrnum]>0.0)
				{
					fl=1;
					break;
				}
			}
			if(fl==0)
			{
				cout<<"Unbounded Solution\n";
				return 0;
			}
			iter++;
			continue;
		}
	}
	return 0;
}

//To find Zj-Cj after each stage of our cycle
void calculate(vector<string>cs, int iter, int extra_var, int total_var, vector<double>& c, vector<double>& z, vector<double>& diff, vector<double>& cb, vector<vector<double> > A)
{
	for(int i=0;i<total_var;i++)
	{
		for(int j=0;j<extra_var;j++)
		{
			z[i]+=(cb[j]*A[j][i]);
		}
	}
	for(int i=0;i<total_var;i++)
	{
		diff.push_back(z[i]-c[i]);
	}
	cout<<"Values of zj-cj "<<iter<<"\n";
	for(int i=0;i<total_var;i++)
	{
		cout<<diff[i]<<" ";
	}
	cout<<"\n";
	cout<<"Values of zj-cj along with the variables for iteration "<<iter<<"\n";
	for(int i=0;i<total_var;i++)
	{
		cout<<cs[i]<<" "<<diff[i];
		cout<<"\n";
	}
	cout<<"\n";
}

//To print basic variables along with their ratios
void calc_pivot(int iter, vector<string>cbs, int extra_var, int total_var, vector<double>& c, vector<double>& z, vector<double>& diff, vector<double>& cb, vector<vector<double> > A, vector<double>& d, int *pivcol, int *pivrnum)
{
	double minval=diff[0];
	*pivrnum=0;
	for(int i=1;i<total_var;i++)
	{
		if(diff[i]<minval)
		{
			minval=diff[i];
			*pivrnum=i;
		}
	}
	vector<double>pivrow;
	for(int i=0;i<extra_var;i++)
	{
		pivrow.push_back(A[i][*pivrnum]);
	}
	//Column of ratios
	vector<double>ratio;
	for(int i=0;i<extra_var;i++)
	{
		if(pivrow[i]>0.0)
		{
			ratio.push_back(((d[i]*1.0)/pivrow[i]));
		}
		else
		{
			double valuev=10000;
			ratio.push_back(valuev*1.0);
		}
	}
	cout<<"Column of ratios with respect to the pivot element for iteration "<<iter<<" is \n";
	for(int i=0;i<extra_var;i++)
	{
		cout<<ratio[i]<<" ";
	}
	cout<<"\n";
	cout<<"Column of ratios with respect to the pivot element along with basic variables "<<iter<<" is \n";
	for(int i=0;i<extra_var;i++)
	{
		cout<<cbs[i]<<" "<<ratio[i]<<"\n";
	}
	cout<<"\n";
	//Pivot column is minmum ratio column
	double mincol=ratio[0];
	*pivcol=0;
	for(int i=0;i<extra_var;i++)
	{
		if(ratio[i]<mincol)
		{
			mincol=ratio[i];
			*pivcol=i;
		}
	}
	cout<<"Pivot Row inside us "<<*pivcol<<"\n";
	vector<double>pivcolmn;
	for(int i=0;i<total_var;i++)
	{
		pivcolmn.push_back(A[*pivcol][i]);
	}
	pivcolmn.clear();
	pivrow.clear();
	ratio.clear();	
}

void table_gen(int iter, int extra_var, int total_var, vector<vector<double> >&A, vector<double> &d, int pivrnum, int pivcol)
{
	double pivele=A[pivcol][pivrnum];
	cout<<"The pivot is "<<pivele<<"\n";
	cout<<"Pivot Row is "<<pivcol<<"\n";
	cout<<"Pivot Column is "<<pivrnum<<"\n";
	for(int i=0;i<total_var;i++)
	{
		A[pivcol][i]=A[pivcol][i]/pivele;
	}
	d[pivcol]=d[pivcol]/pivele;
	//update remaining A
	for(int i=0;i<extra_var;i++)
	{
		if(i!=pivcol)
		{
			double vall=A[i][pivrnum];
			d[i]=d[i]-(vall*d[pivcol]);
			for(int j=0;j<total_var;j++)
			{
				A[i][j]-=(vall*A[pivcol][j]);
			}	
		}
	}
	//Display A
	cout<<"Simplex table for iteration "<<iter<<" \n";
	for(int i=0;i<extra_var;i++)
	{
		for(int j=0;j<total_var;j++)
		{
			cout<<A[i][j]<<" ";
		}
		cout<<d[i]<<" ";
		cout<<"\n";
		
	}
	cout<<"\n";	
}
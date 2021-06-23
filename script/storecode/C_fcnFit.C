TNtupleD* nt = nullptr;

// 2 gaussian + polynomial
// par[0]:c1, par[2]:c2
// par[3]:numSig, par[4]:numBkg
double model(double x, double* par)
{
    // build double gaussians
    const double mu=5.6185;
    const double bsMultiplier=0.86678;
    const frac = 0.71056;

    // build gaussian1
    double sigma1=0.0093315;
    sigma1*=bsMultiplier;
    double norm1Inv=sqrt(2.*TMath::Pi())*sigma1;
    double pdfVal1 = exp(-0.5*pow((x-mu)/sigma1,2))/norm1Inv;

    double sigma2=0.024014;
    sigma2*=bsMultiplier;
    double norm2Inv=sqrt(2.*TMath::Pi())*sigma1;
    
    
}
void fcn(int& npar, double* gin, double& f, double* par, int iflag)
{
    double c1=

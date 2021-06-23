{
    TFile* file = TFile::Open("result_flatNtuple_LbL0_preSelection_noKinematicCut.root");
    TNtupleD* ntP = (TNtupleD*) file->Get("pLbL0/2016Data");
    TNtupleD* ntN = (TNtupleD*) file->Get("nLbL0/2016Data");
    TNtupleD* ntPMC = (TNtupleD*) file->Get("pLbL0/LbL0");
    TNtupleD* ntNMC = (TNtupleD*) file->Get("nLbL0/LbLo");

    TCanvas* c1 = new TCanvas("c1","",1000,1000);
    c1->Divide(2,2);
    c1->cd(1);
    //ntP->Draw("lbl0Mass","lbl0Mass>5.4&&lbl0Mass<5.9&&tktkMass>1.10&&tktkMass<1.130");
    ntP->Draw("tktkMass","lbl0Mass>5.55&&lbl0Mass<5.7&&tktkMass>1.1&&tktkMass<1.14");
    c1->cd(2);
    //ntN->Draw("lbl0Mass","lbl0Mass>5.4&&lbl0Mass<5.9&&tktkMass>1.10&&tktkMass<1.130");
    ntN->Draw("tktkMass","lbl0Mass>5.55&&lbl0Mass<5.7&&tktkMass>1.1&&tktkMass<1.14");
    c1->cd(3);
    ntPMC->Draw("tktkMass","lbl0Mass>5.55&&lbl0Mass<5.7&&tktkMass>1.1&&tktkMass<1.14");
    c1->cd(4);
    ntNMC->Draw("tktkMass","lbl0Mass>5.55&&lbl0Mass<5.7&&tktkMass>1.1&&tktkMass<1.14");
}

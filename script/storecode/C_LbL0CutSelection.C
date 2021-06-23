{
    std::string outName = "store_fig/SeparatePt";
    bool totRange = true;
    bool ptRange1 = true;
    bool ptRange2 = true;
    bool ptMinRange = true;

    TFile* fileS = TFile::Open("result_flatNtuple_LbTk_preSelection_noKinematicCut.root");
    TFile* fileB = TFile::Open("result_flatNtuple_LbL0_preSelection_noKinematicCut.root");
    TNtupleD* ntSP = (TNtupleD*) fileS->Get("pLbTk/2016Data");
    TNtupleD* ntSN = (TNtupleD*) fileS->Get("nLbTk/2016Data");
    TNtupleD* ntBP = (TNtupleD*) fileB->Get("pLbL0/2016Data");
    TNtupleD* ntBN = (TNtupleD*) fileB->Get("nLbL0/2016Data");
    TH1D* h1 = new TH1D("h1","#Lambda^{0}_{b}#rightarrow J/#psi #Lambda^{0}",50,5.4,5.9);
    TH1D* h2 = new TH1D("h2","#bar{#Lambda}^{0}_{b}#rightarrow J/#psi #bar{#Lambda}^{0}",50,5.4,5.9);
    TH1D* h3 = new TH1D("h3","#Lambda^{0}_{b}#rightarrow J/#psi p K^{-}",50,5.4,5.9);
    TH1D* h4 = new TH1D("h4","#bar{#Lambda}^{0}_{b}#rightarrow J/#psi #bar{p} K^{+}",50,5.4,5.9);

    char totCut[300];
    const char* lbl0Cut="lbl0Mass>5.4&&lbl0Mass<5.9&&tktkMass>1.105&&tktkMass<1.130";
    const char* lbTKCut="lbtkMass>5.4&&lbtkMass<5.9";
    const char* lbtkCut="lbtkbarMass>5.4&&lbtkbarMass<5.9";
    const char* lbl0PtCut="lbl0Pt";
    const char* lbtkPtCut="lbtkPt";

    std::string minCutVal = "";
    std::string maxCutVal = "";


    TCanvas* c1 = new TCanvas("c1","",800,800);
    c1->Divide(2,2);
    for ( int i=4; i>0; --i )
    {
        TPad* p = (TPad*) c1->GetPad(i);
        p->SetFillColor(4000);
        p->SetFillStyle(4000);
    }
        
    c1->SetFillStyle(4000);
    c1->SetFillColor(4000);
    std::string a = outName+".pdf";
    const char* pdf = a.c_str();
    c1->SaveAs( (outName+".pdf[").c_str() );

    if ( totRange )
    {
        sprintf( totCut, "%s", lbl0Cut);
        c1->cd(1); ntBP->Draw("lbl0Mass>>h1",totCut);
        h1->Draw();
        cout << h1->GetEntries() << endl;
        c1->cd(3); ntBN->Draw("lbl0Mass>>h2",totCut);

        sprintf( totCut, "%s", lbTKCut);
        c1->cd(2); ntSP->Draw("lbtkMass>>h3",totCut);
        sprintf( totCut, "%s", lbtkCut);
        c1->cd(4); ntSN->Draw("lbtkbarMass>>h4",totCut);
        c1->SaveAs(pdf);
        c1->SaveAs( (outName+"_TotRange.eps").c_str() );
    }
    {
        minCutVal = "20.";
        maxCutVal = "30.";
        sprintf( totCut, "%s && %s>%s && %s<%s", lbl0Cut,lbl0PtCut, minCutVal.c_str(), lbl0PtCut, maxCutVal.c_str() );
        c1->cd(1); ntBP->Draw("lbl0Mass>>h1",totCut);
        h1->Draw();
        c1->cd(3); ntBN->Draw("lbl0Mass>>h2",totCut);

        sprintf( totCut, "%s && %s>%s && %s<%s", lbTKCut,lbtkPtCut, minCutVal.c_str(), lbtkPtCut, maxCutVal.c_str() );
        c1->cd(2); ntSP->Draw("lbtkMass>>h3",totCut);
        sprintf( totCut, "%s && %s>%s && %s<%s", lbtkCut,lbtkPtCut, minCutVal.c_str(), lbtkPtCut, maxCutVal.c_str() );
        c1->cd(4); ntSN->Draw("lbtkbarMass>>h4",totCut);
        c1->SaveAs(pdf);
        c1->SaveAs( (outName+"_"+minCutVal+"To"+maxCutVal+".eps").c_str() );
    }
    {
        minCutVal = "30.";
        maxCutVal = "33.";
        sprintf( totCut, "%s && %s>%s && %s<%s", lbl0Cut,lbl0PtCut, minCutVal.c_str(), lbl0PtCut, maxCutVal.c_str() );
        c1->cd(1); ntBP->Draw("lbl0Mass>>h1",totCut);
        h1->Draw();
        c1->cd(3); ntBN->Draw("lbl0Mass>>h2",totCut);

        sprintf( totCut, "%s && %s>%s && %s<%s", lbTKCut,lbtkPtCut, minCutVal.c_str(), lbtkPtCut, maxCutVal.c_str() );
        c1->cd(2); ntSP->Draw("lbtkMass>>h3",totCut);
        sprintf( totCut, "%s && %s>%s && %s<%s", lbtkCut,lbtkPtCut, minCutVal.c_str(), lbtkPtCut, maxCutVal.c_str() );
        c1->cd(4); ntSN->Draw("lbtkbarMass>>h4",totCut);
        c1->SaveAs(pdf);
        c1->SaveAs( (outName+"_"+minCutVal+"To"+maxCutVal+".eps").c_str() );
    }
    {
        minCutVal = "33.";
        maxCutVal = "38.";
        sprintf( totCut, "%s && %s>%s && %s<%s", lbl0Cut,lbl0PtCut, minCutVal.c_str(), lbl0PtCut, maxCutVal.c_str() );
        c1->cd(1); ntBP->Draw("lbl0Mass>>h1",totCut);
        h1->Draw();
        c1->cd(3); ntBN->Draw("lbl0Mass>>h2",totCut);

        sprintf( totCut, "%s && %s>%s && %s<%s", lbTKCut,lbtkPtCut, minCutVal.c_str(), lbtkPtCut, maxCutVal.c_str() );
        c1->cd(2); ntSP->Draw("lbtkMass>>h3",totCut);
        sprintf( totCut, "%s && %s>%s && %s<%s", lbtkCut,lbtkPtCut, minCutVal.c_str(), lbtkPtCut, maxCutVal.c_str() );
        c1->cd(4); ntSN->Draw("lbtkbarMass>>h4",totCut);
        c1->SaveAs(pdf);
        c1->SaveAs( (outName+"_"+minCutVal+"To"+maxCutVal+".eps").c_str() );
    }
    {
        minCutVal = "38.";
        maxCutVal = "45.";
        sprintf( totCut, "%s && %s>%s && %s<%s", lbl0Cut,lbl0PtCut, minCutVal.c_str(), lbl0PtCut, maxCutVal.c_str() );
        c1->cd(1); ntBP->Draw("lbl0Mass>>h1",totCut);
        h1->Draw();
        c1->cd(3); ntBN->Draw("lbl0Mass>>h2",totCut);

        sprintf( totCut, "%s && %s>%s && %s<%s", lbTKCut,lbtkPtCut, minCutVal.c_str(), lbtkPtCut, maxCutVal.c_str() );
        c1->cd(2); ntSP->Draw("lbtkMass>>h3",totCut);
        sprintf( totCut, "%s && %s>%s && %s<%s", lbtkCut,lbtkPtCut, minCutVal.c_str(), lbtkPtCut, maxCutVal.c_str() );
        c1->cd(4); ntSN->Draw("lbtkbarMass>>h4",totCut);
        c1->SaveAs(pdf);
        c1->SaveAs( (outName+"_"+minCutVal+"To"+maxCutVal+".eps").c_str() );
    }
//    {
//        minCutVal = "45.";
//        maxCutVal = "65.";
//        sprintf( totCut, "%s && %s>%s && %s<%s", lbl0Cut,lbl0PtCut, minCutVal.c_str(), lbl0PtCut, maxCutVal.c_str() );
//        c1->cd(1); ntBP->Draw("lbl0Mass>>h1",totCut);
//        h1->Draw();
//        c1->cd(2); ntBN->Draw("lbl0Mass>>h2",totCut);
//
//        sprintf( totCut, "%s && %s>%s && %s<%s", lbTKCut,lbtkPtCut, minCutVal.c_str(), lbtkPtCut, maxCutVal.c_str() );
//        c1->cd(3); ntSP->Draw("lbtkMass>>h3",totCut);
//        sprintf( totCut, "%s && %s>%s && %s<%s", lbtkCut,lbtkPtCut, minCutVal.c_str(), lbtkPtCut, maxCutVal.c_str() );
//        c1->cd(4); ntSN->Draw("lbtkbarMass>>h4",totCut);
//        c1->SaveAs(pdf);
//        c1->SaveAs( (outName+"_"+minCutVal+"To"+maxCutVal+".eps").c_str() );
//    }
    if ( ptMinRange )
    {
        minCutVal = "45.";
        sprintf( totCut, "%s && %s>%s", lbl0Cut,lbl0PtCut, minCutVal.c_str() );
        c1->cd(1); ntBP->Draw("lbl0Mass>>h1",totCut);
        c1->cd(3); ntBN->Draw("lbl0Mass>>h2",totCut);

        sprintf( totCut, "%s && %s>%s", lbTKCut,lbtkPtCut, minCutVal.c_str() );
        c1->cd(2); ntSP->Draw("lbtkMass>>h3",totCut);
        sprintf( totCut, "%s && %s>%s", lbtkCut,lbtkPtCut, minCutVal.c_str() );
        c1->cd(4); ntSN->Draw("lbtkbarMass>>h4",totCut);
        c1->SaveAs(pdf);
        c1->SaveAs( (outName+"_Bigger"+minCutVal+".eps").c_str() );
    }


    c1->SaveAs( (outName+".pdf]").c_str() );
}


{
    TFile* f = TFile::Open("storeroot/tReduced/tree_forGA_removeBsBdOnly/data_2017RunBCDEF.root");
    TTree* t = (TTree*)f->Get("lbSpecificDecay/pnLbTk");
    TCanvas* c1 = new TCanvas("c1","", 1600, 1000);
    c1->SaveAs("storefig/htesting.pdf[");
    char tightCuts[512];
    char looseCuts[512];
    char cutWithFrame[512];

    char basicpCut[]="ptargetJpsiP_mass<4.9&&pptonPt>3.";
    char basicnCut[]="ntargetJpsiP_mass<4.9&&nptonPt>3.";
    char notpLb[]="(plbtkMass<5.619-0.03||plbtkMass>5.619+0.03)";
    char notnLb[]="(nlbtkMass<5.619-0.03||nlbtkMass>5.619+0.03)";
    char pLbFrame[]="(plbtkMass>5.45&&plbtkMass<5.75)";
    char nLbFrame[]="(nlbtkMass>5.45&&nlbtkMass<5.75)";
    char notpBdToKstar892[]="!(pfake_BdMass>5.2&&pfake_BdMass<5.35&&pfake_KstarMass>0.7&&pfake_KstarMass<1.1)";
    char notnBdToKstar892[]="!(nfake_BdMass>5.2&&nfake_BdMass<5.35&&nfake_KstarMass>0.7&&nfake_KstarMass<1.1)";
    char notpBdToKstar1430[]="!(pfake_BdMass>5.2&&pfake_BdMass<5.35&&pfake_KstarMass>1.3&&pfake_KstarMass<1.5)";
    char notnBdToKstar1430[]="!(nfake_BdMass>5.2&&nfake_BdMass<5.35&&nfake_KstarMass>1.3&&nfake_KstarMass<1.5)";
    char focusOnpBdTopipi[]="(pfake_mumupipiMass>5.24&&pfake_mumupipiMass<5.32)";
    char focusOnnBdTopipi[]="(nfake_mumupipiMass>5.24&&nfake_mumupipiMass<5.32)";

    sprintf(tightCuts, "%s&&%s&&%s&&%s&&%s", basicpCut, notnBdToKstar892, notpBdToKstar892, notpBdToKstar1430, notnBdToKstar1430);
    sprintf(looseCuts, "%s&&%s&&%s", basicpCut, notnBdToKstar892, notpBdToKstar892);
    //sprintf(looseCuts, "%s&&%s&&%s", basicCut, notpLb, notnLb);
    t->Draw("pfake_BdMass>>noCutpBd");
    c1->SaveAs("storefig/htesting.pdf");
    t->Draw("pfake_BdMass>>loosepBd", looseCuts);
    c1->SaveAs("storefig/htesting.pdf");
    t->Draw("pfake_BdMass", tightCuts);
    c1->SaveAs("storefig/htesting.pdf");
    t->Draw("pfake_KstarMass>>loosepKstar", looseCuts);
    c1->SaveAs("storefig/htesting.pdf");
    t->Draw("pfake_KstarMass", tightCuts);
    c1->SaveAs("storefig/htesting.pdf");

    t->Draw("nfake_BdMass>>noCutnBd");
    c1->SaveAs("storefig/htesting.pdf");
    t->Draw("nfake_BdMass>>loosenBd", looseCuts);
    c1->SaveAs("storefig/htesting.pdf");
    t->Draw("nfake_BdMass", tightCuts);
    c1->SaveAs("storefig/htesting.pdf");
    t->Draw("nfake_KstarMass>>loosenKstar", looseCuts);
    c1->SaveAs("storefig/htesting.pdf");
    t->Draw("nfake_KstarMass", tightCuts);
    c1->SaveAs("storefig/htesting.pdf");


    t->Draw("pfake_BsMass", tightCuts);
    c1->SaveAs("storefig/htesting.pdf");
    t->Draw("nfake_BsMass", tightCuts);
    c1->SaveAs("storefig/htesting.pdf");

    // plot p Lb in massFrame with cuts
    sprintf(cutWithFrame, "%s&&%s", looseCuts, pLbFrame);
    t->Draw("plbtkMass>>loosepLb_pBasicCut", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(cutWithFrame, "%s&&%s", tightCuts, pLbFrame);
    t->Draw("plbtkMass>>tightpLb_pBasicCut", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(cutWithFrame, "%s&&%s", looseCuts, nLbFrame);
    t->Draw("nlbtkMass>>loosenLb_pBasicCut", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(cutWithFrame, "%s&&%s", tightCuts, nLbFrame);
    t->Draw("nlbtkMass>>tightnLb_pBasicCut", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(cutWithFrame, "%s", pLbFrame);
    t->Draw("plbtkMass>>noCutpLb", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");

    // plot n Lb in massFrame with cuts
    sprintf(tightCuts, "%s&&%s&&%s&&%s&&%s", basicnCut, notnBdToKstar892, notpBdToKstar892, notpBdToKstar1430, notnBdToKstar1430);
    sprintf(looseCuts, "%s&&%s&&%s", basicnCut, notnBdToKstar892, notpBdToKstar892);
    sprintf(cutWithFrame, "%s&&%s", looseCuts, pLbFrame);
    t->Draw("plbtkMass>>loosepLb_nBasicCut", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(cutWithFrame, "%s&&%s", tightCuts, pLbFrame);
    t->Draw("plbtkMass>>tightpLb_nBasicCut", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(cutWithFrame, "%s&&%s", looseCuts, nLbFrame);
    t->Draw("nlbtkMass>>loosenLb_nBasicCut", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(cutWithFrame, "%s&&%s", tightCuts, nLbFrame);
    t->Draw("nlbtkMass>>tightnLb_nBasicCut", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(cutWithFrame, "%s", nLbFrame);
    t->Draw("nlbtkMass>>noCutnLb", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");


    // // plot p Lb in massFrame with pbasic success but nbasic failed
    sprintf(tightCuts, "%s&&!%s&&%s&&%s&&%s&&%s", basicpCut, basicnCut, notnBdToKstar892, notpBdToKstar892, notpBdToKstar1430, notnBdToKstar1430);
    sprintf(cutWithFrame, "%s&&%s", tightCuts, pLbFrame);
    t->Draw("plbtkMass>>pLb_pBasicCut_failednBasicCut", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(tightCuts, "%s&&!%s&&%s&&%s&&%s&&%s", basicnCut, basicpCut, notnBdToKstar892, notpBdToKstar892, notpBdToKstar1430, notnBdToKstar1430);
    sprintf(cutWithFrame, "%s&&%s", tightCuts, nLbFrame);
    t->Draw("nlbtkMass>>nLb_nBasicCut_failedpBasicCut", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");


    // plot Lb in massFrame if pton Pt > kaon Pt
    sprintf(tightCuts, "%s&&(pptonPt>pkaonPt)&&%s&&%s&&%s&&%s", basicpCut, notnBdToKstar892, notpBdToKstar892, notpBdToKstar1430, notnBdToKstar1430);
    sprintf(cutWithFrame, "%s&&%s", tightCuts, pLbFrame);
    t->Draw("plbtkMass>>pLb_pBasicCut_ptonBkaon", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(tightCuts, "%s&&(nptonPt>nkaonPt)&&%s&&%s&&%s&&%s", basicnCut, notnBdToKstar892, notpBdToKstar892, notpBdToKstar1430, notnBdToKstar1430);
    sprintf(cutWithFrame, "%s&&%s", tightCuts, nLbFrame);
    t->Draw("nlbtkMass>>nLb_nBasicCut_ptonBkaon", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");

    // plot Lb in massFrame if pton Pt < kaon Pt
    sprintf(tightCuts, "%s&&(pptonPt<pkaonPt)&&%s&&%s&&%s&&%s", basicpCut, notnBdToKstar892, notpBdToKstar892, notpBdToKstar1430, notnBdToKstar1430);
    sprintf(cutWithFrame, "%s&&%s", tightCuts, pLbFrame);
    t->Draw("plbtkMass>>pLb_pBasicCut_ptonSkaon", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(tightCuts, "%s&&(nptonPt<nkaonPt)&&%s&&%s&&%s&&%s", basicnCut, notnBdToKstar892, notpBdToKstar892, notpBdToKstar1430, notnBdToKstar1430);
    sprintf(cutWithFrame, "%s&&%s", tightCuts, nLbFrame);
    t->Draw("nlbtkMass>>nLb_nBasicCut_ptonSkaon", cutWithFrame);
    c1->SaveAs("storefig/htesting.pdf");

    char spCuts[512];
    sprintf(spCuts, "%s&&%s", tightCuts, focusOnpBdTopipi);
    t->Draw("nfake_KshortMass", spCuts);
    c1->SaveAs("storefig/htesting.pdf");
    sprintf(spCuts, "%s&&%s", tightCuts, focusOnnBdTopipi);
    t->Draw("nfake_mumupipiMass", spCuts);
    c1->SaveAs("storefig/htesting.pdf");







    c1->SaveAs("storefig/htesting.pdf]");
}



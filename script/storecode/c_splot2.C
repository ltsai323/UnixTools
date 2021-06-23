/////////////////////////////////////////////////////////////////////////
//
// SPlot tutorial
// author: Kyle Cranmer
// date Dec. 2008 
//
// This tutorial shows an example of using SPlot to unfold two distributions.
// The physics context for the example is that we want to know 
// the isolation distribution for real electrons from Z events 
// and fake electrons from QCD.  Isolation is our 'control' variable
// To unfold them, we need a model for an uncorrelated variable that
// discriminates between Z and QCD.  To do this, we use the invariant 
// mass of two electrons.  We model the Z with a Gaussian and the QCD
// with a falling exponential.
//
// Note, since we don't have real data in this tutorial, we need to generate
// toy data.  To do that we need a model for the isolation variable for
// both Z and QCD.  This is only used to generate the toy data, and would
// not be needed if we had real data.
/////////////////////////////////////////////////////////////////////////

#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooStats/SPlot.h"
#include "RooDataSet.h"
#include "RooRealVar.h"
#include "RooGaussian.h"
#include "RooExponential.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooProdPdf.h"
#include "RooAddition.h"
#include "RooProduct.h"
#include "TCanvas.h"
#include "RooAbsPdf.h"
#include "RooFit.h"
#include "RooFitResult.h"
#include "RooWorkspace.h"
#include "RooConstVar.h"

// use this order for safety on library loading
using namespace RooFit;
using namespace RooStats;


// see below for implementation
void AddModel(RooWorkspace *);
void AddData(RooWorkspace *);
void DoSPlot(RooWorkspace *);
void MakePlots(RooWorkspace *);
double treeEntries;

void setSignalRegion( double mean, double sigma );
bool inSignalRegion( double mass );
double mMass, MMass;
bool sigRegionSet = false;


void splot2()
{

    // Create a new workspace to manage the project.
    RooWorkspace *wspace = new RooWorkspace("myWS");

    // add some toy data to the workspace
    AddData(wspace);

    // add the signal and background models to the workspace.
    // Inside this function you will find a discription our model.
    AddModel(wspace);

    // inspect the workspace if you wish
    //  wspace->Print();

    // do sPlot.  
    //This wil make a new dataset with sWeights added for every event.
    DoSPlot(wspace);

    // Make some plots showing the discriminating variable and 
    // the control variable after unfolding.
    MakePlots(wspace);

    // cleanup
    delete wspace;

}


//____________________________________
void AddModel(RooWorkspace * ws)
{

    // Make models for signal (Higgs) and background (Z+jets and QCD)
    // In real life, this part requires an intellegent modeling 
    // of signal and background -- this is only an example.  

    // make a RooRealVar for the observables
    RooRealVar *lbtkMass = ws->var("plbtkMass");
    RooRealVar *targetJpsiP_Mass = ws->var("ptargetJpsiP_mass");


    /////////////////////////////////////////////
    // make lambda B model
    RooRealVar par_mean("mean", "parameter to gaussian: mean", 5.620, 5.55, 5.7);
    RooRealVar par_width("width", "parameter to gaussian: width", 0.01, 0.000001, 10.);
    RooGaussian pdf_gaus("gaus", "PDF : gaussian", *lbtkMass, par_mean, par_width);

    // we know lambdaB mass
    //par_mean.setConstant();

    //////////////////////////////////////////////
    // background model

    RooRealVar par_ch1("ch1", "parameter to chebychev : 1st order", -0.5, -10., 10.);
    RooRealVar par_ch2("ch2", "parameter to chebychev : 2nd order", -0.05, -10., 10.);
    RooRealVar par_ch3("ch3", "parameter to chebychev : 3rd order", -0.008, -10., 10.);
    RooRealVar par_ch4("ch4", "parameter to chebychev : 4rd order", 0.02, -10., 10.);
    RooChebychev pdf_cheb("cheb", "PDF : chebychev", *lbtkMass, RooArgSet(par_ch1, par_ch2, par_ch3, par_ch4));



    //////////////////////////////////////////////
    // combined model

    RooRealVar lbSigYield("lbSigYield", "fitted signal yield in lb mass frame", treeEntries / 100., 0., treeEntries);
    RooRealVar lbBkgYield("lbBkgYield", "fitted background yield in lb mass frame", treeEntries, 0., treeEntries);

    // now make the combined model
    RooAddPdf lbModel("lbModel", "s+b model in lb mass frame", RooArgList(pdf_gaus, pdf_cheb),
                      RooArgList(lbSigYield, lbBkgYield));

    // interesting for debugging and visualizing the model
    lbModel.graphVizTree("fullModel.dot");


    ws->import(lbModel);
    return;
}

//____________________________________
void AddData(RooWorkspace * ws)
{
    // get what we need out of the workspace to make toy data
    RooRealVar lbMass("plbtkMass", "#Lambda^{0}_{b} mass", 5.4, 5.9, "GeV");
    RooRealVar pQMass("ptargetJpsiP_mass", "j/#psi+p mass", 4.0, 4.85, "GeV");
    RooRealVar lbPt("plbtkPt", "#Lambda^{0}_{b} pt distribution", 0., 100., "GeV");
    RooRealVar lbFD2dSig("plbtkFDSig", "flight distance significance", 3., 20., "");
    // import a dataset
    TFile *readFile = TFile::Open("storeroot/tReduced/tree_forGA_removeBsBdOnly/data_2016RunBCDEFGH.root");
    //TFile *readFile = TFile::Open("storeroot/tReduced/tree_forGA_removeBsBdOnly/data_2017RunBCDEF.root");
    //TFile *readFile = TFile::Open("storeroot/tReduced/tree_forGA_removeBsBdOnly/totdata_16and17.root");
    TTree *readTree = (TTree *) readFile->Get("lbSpecificDecay/pnLbTk");
    treeEntries = readTree->GetEntries();
    RooDataSet readOrigData("readOrigData", "readOrigData", RooArgSet(lbMass, pQMass, lbFD2dSig), RooFit::Import(*readTree));
    RooDataSet* readData = (RooDataSet*)readOrigData.reduce("ptargetJpsiP_mass<4.85");

    ws->import(*readData, Rename("readData"));
    readFile->Close();
    return;

}

//____________________________________
void DoSPlot(RooWorkspace * ws)
{

    // get what we need out of the workspace to do the fit
    RooAbsPdf *model = ws->pdf("lbModel");
    RooRealVar *lbSigYield = ws->var("lbSigYield");
    RooRealVar *lbBkgYield = ws->var("lbBkgYield");
    RooDataSet *data = (RooDataSet *) ws->data("readData");


    // fit the model to the data.
    model->fitTo(*data, Extended());

    // The sPlot technique requires that we fix the parameters
    // of the model that are not yields after doing the fit.
    RooRealVar* par_mean = ws->var("mean");
    RooRealVar *par_width = ws->var("width");
    par_width->setConstant();
    setSignalRegion( par_mean->getVal(), par_width->getVal() );

    RooMsgService::instance().setSilentMode(true);


    // Now we use the SPlot class to add SWeights to our data set
    // based on our model and our yield variables
    RooStats::SPlot * sData = new RooStats::SPlot("sData", "An SPlot",
                                                  *data, model, RooArgList(*lbSigYield, *lbBkgYield));


    // Check that our weights have the desired properties

    std::cout << "Check SWeights:" << std::endl;


    std::cout << std::endl << "Yield of sig in lb mass frame: "
        << lbSigYield->getVal() << ".  From sWeights is: " << sData->GetYieldFromSWeight("lbSigYield") << std::endl;

    std::cout << std::endl << "Yield of bkg in lb mass frame: "
        << lbBkgYield->getVal() << ".  From sWeights is: " << sData->GetYieldFromSWeight("lbBkgYield") << std::endl;

    for (Int_t i = 0; i < 10; i++) {
        std::cout << "lb sig Weight   " << sData->GetSWeight(i, "lbSigYield")
               << "   lb bkg Weight   " << sData->GetSWeight(i, "lbBkgYield")
               << "  Total Weight   " << sData->GetSumOfEventSWeight(i)
               << std::endl;
    }

    std::cout << std::endl;

    // import this new dataset with sWeights
    ws->import(*data, Rename("dataWithSWeights"));


}

void MakePlots(RooWorkspace * ws)
{

    // Here we make plots of the discriminating variable (invMass) after the fit
    // and of the control variable (isolation) after unfolding with sPlot.

    // make our canvas
    TCanvas *cdata = new TCanvas("sPlot", "sPlot demo", 1600, 1000);
    cdata->Divide(1, 3);

    // get what we need out of the workspace
    RooAbsPdf *totModel = ws->pdf("lbModel");
    RooAbsPdf *lbSigModel = ws->pdf("gaus");
    RooAbsPdf *lbBkgModel = ws->pdf("cheb");

    RooRealVar *lbMass = ws->var("plbtkMass");
    RooRealVar *pQMass = ws->var("ptargetJpsiP_mass");
    //RooRealVar *lbPt   = ws->var("plbtkPt");
    RooRealVar *fdSig  = ws->var("plbtkFDSig");

    // note, we get the dataset with sWeights
    RooDataSet *data = (RooDataSet *) ws->data("dataWithSWeights");

    // this shouldn't be necessary, need to fix something with workspace
    // do this to set parameters back to their fitted values.
    totModel->fitTo(*data, Extended());

    //plot invMass for data with full model and individual componenets overlayed
    //  TCanvas* cdata = new TCanvas();
    cdata->cd(1);
    RooPlot *frame = lbMass->frame();
    data->plotOn(frame);
    totModel->plotOn(frame);
    totModel->plotOn(frame, Components(*lbSigModel), LineStyle(kDashed), LineColor(kRed));
    totModel->plotOn(frame, Components(*lbBkgModel), LineStyle(kDashed), LineColor(kGreen));

    frame->SetTitle("Fit of model to discriminating variable");
    frame->Draw();

    // Now use the sWeights to show isolation distribution for Z and QCD.  
    // The SPlot class can make this easier, but here we demonstrait in more
    // detail how the sWeights are used.  The SPlot class should make this 
    // very easy and needs some more development.

    // Plot isolation for Z component.  
    // Do this by plotting all events weighted by the sWeight for the Z component.
    // The SPlot class adds a new variable that has the name of the corresponding
    // yield + "_sw".
    cdata->cd(2);

    // create weightfed data set 
    RooDataSet *dataw_sig =
        new RooDataSet(data->GetName(), data->GetTitle(), data, *data->get(), 0, "lbSigYield_sw");

    RooPlot *frame2 = pQMass->frame();
    dataw_sig->plotOn(frame2, DataError(RooAbsData::SumW2));

    frame2->SetTitle("sig with sWeight, in jpsi+p massWindow");
    frame2->Draw();

    // Plot isolation for QCD component.  
    // Eg. plot all events weighted by the sWeight for the QCD component.
    // The SPlot class adds a new variable that has the name of the corresponding
    // yield + "_sw".
    cdata->cd(3);
    RooDataSet *dataw_bkg =
        new RooDataSet(data->GetName(), data->GetTitle(), data, *data->get(), 0, "lbBkgYield_sw");
    RooPlot *frame3 = pQMass->frame();
    dataw_bkg->plotOn(frame3, DataError(RooAbsData::SumW2));

    frame3->SetTitle("bkg with sWeight, in jpsi+p massWindow");
    frame3->Draw();

    cdata->SaveAs("storefig/sPlot.pdf[");
    cdata->SaveAs("storefig/sPlot.pdf");
    cdata->SaveAs("storefig/sPlot.eps");

    cdata->Clear();
    frame->Draw();
    cdata->SaveAs("storefig/sPlot.LbFittingRes.eps");
    frame2->Draw();
    cdata->SaveAs("storefig/sPlot.jpsipMass.signal.eps");
    frame3->Draw();
    cdata->SaveAs("storefig/sPlot.jpsipMass.background.eps");

    RooPlot* fdFrame = fdSig->frame();
    dataw_sig->plotOn(fdFrame, DataError(RooAbsData::SumW2));
    fdFrame->SetTitle("");
    fdFrame->Draw();
    cdata->SaveAs("storefig/sPlot.pdf");
    cdata->SaveAs("storefig/sPlot.FDsig.SIG.eps");
    RooPlot* fdframe = fdSig->frame();
    dataw_bkg->plotOn(fdframe, DataError(RooAbsData::SumW2));
    fdframe->SetTitle("");
    fdframe->Draw();
    cdata->SaveAs("storefig/sPlot.pdf");
    cdata->SaveAs("storefig/sPlot.FDsig.BKG.eps");

    cdata->Clear();
    cdata->cd();
    RooPlot* pqmassFrame = pQMass->frame();
    dataw_sig->plotOn(pqmassFrame, DataError(RooAbsData::SumW2), LineColor(30), LineWidth(2), LineStyle(7), Name("pqSig"));
    dataw_bkg->plotOn(pqmassFrame, DataError(RooAbsData::SumW2), LineColor(50), LineWidth(2), LineStyle(7), Name("pqBkg"));
    TGraph* objPQSig = (TGraph*) pqmassFrame->findObject("pqSig");
    TGraph* objPQBkg = (TGraph*) pqmassFrame->findObject("pqBkg");
    TLegend* leg = new TLegend(0.2, 0.6, 0.45, 0.85);
    leg->SetLineColor(0);
    leg->SetFillStyle(4000);
    leg->SetFillStyle(4000);
    leg->AddEntry( objPQSig, "signal in #Lambda^{0}_{b}", "L" );
    leg->AddEntry( objPQBkg, "backgd in #Lambda^{0}_{b}", "L" );
    pqmassFrame->SetTitle("compare jpsiP mass with sWeight");

    pqmassFrame->Draw();
    leg->Draw("same");
    cdata->SaveAs("storefig/sPlot.jpsipMass.SIGandBKG.eps");
    cdata->SaveAs("storefig/sPlot.pdf");
    
    RooPlot* lbmassFrame = lbMass->frame();
    data->plotOn(lbmassFrame);
    totModel->plotOn(lbmassFrame);
    totModel->plotOn(lbmassFrame, Components(*lbSigModel), LineStyle(kDashed), LineColor(kRed)  , Name("lbsigModelplot"));
    totModel->plotOn(lbmassFrame, Components(*lbBkgModel), LineStyle(kDashed), LineColor(kGreen), Name("lbbkgModelplot"));
    TGraph* objlbSig = (TGraph*) lbmassFrame->findObject("lbsigModelplot");
    TGraph* objlbBkg = (TGraph*) lbmassFrame->findObject("lbbkgModelplot");
    TLegend* leg2 = new TLegend( 0.6, 0.6, 0.85, 0.85 );
    leg2->SetLineColor(0);
    leg2->SetFillStyle(4000);
    leg2->SetFillStyle(4000);
    leg2->AddEntry( objlbSig, "signal PDF(Gaus)", "L" );
    leg2->AddEntry( objlbBkg, "backgd PDF(Cheb)", "L" );
    lbmassFrame->SetTitle("Fit of model to discriminating variable");

    lbmassFrame->Draw();
    leg2->Draw("same");
    cdata->SaveAs("storefig/sPlot.lbMass.SIGandBKG.eps");
    cdata->SaveAs("storefig/sPlot.pdf");

    //std::cout << lbPt->getVal() << std::endl;
    //RooPlot* lbptFrame = lbPt->frame();
    //data->plotOn(lbptFrame);
    //totModel->plotOn(lbptFrame);
    //totModel->plotOn(lbptFrame, Components(*lbSigModel), LineStyle(kDashed), LineColor(kRed)  , Name("lbsigModelplot"));
    //totModel->plotOn(lbptFrame, Components(*lbBkgModel), LineStyle(kDashed), LineColor(kGreen), Name("lbbkgModelplot"));
    //TGraph* objlbSig_1 = (TGraph*) lbptFrame->findObject("lbsigModelplot");
    //TGraph* objlbBkg_1 = (TGraph*) lbptFrame->findObject("lbbkgModelplot");
    //TLegend* leg3 = new TLegend( 0.6, 0.6, 0.85, 0.85 );
    //leg3->SetLineColor(0);
    //leg3->SetFillStyle(4000);
    //leg3->SetFillStyle(4000);
    //leg3->AddEntry( objlbSig_1, "signal PDF(Gaus)", "L" );
    //leg3->AddEntry( objlbBkg_1, "backgd PDF(Cheb)", "L" );
    //lbptFrame->SetTitle("Fit of model to discriminating variable");

    //lbptFrame->Draw();
    //leg3->Draw("same");
    //cdata->SaveAs("storefig/sPlot.lbMass.SIGandBKG.eps");
    //cdata->SaveAs("storefig/sPlot.pdf");
    cdata->SaveAs("storefig/sPlot.pdf]");

    delete cdata;
    delete leg, leg2;
    delete dataw_sig, dataw_bkg;
    return;
}

void setSignalRegion( double mean, double sigma )
{
    mMass = mean - 3.0 * sigma;
    MMass = mean + 3.0 * sigma;
    sigRegionSet = true;
    return;
}
bool inSignalRegion( double mass )
{
    if ( !sigRegionSet ) return false;
    if ( mass > MMass )  return false;
    if ( mass < mMass )  return false;
    return true;
}


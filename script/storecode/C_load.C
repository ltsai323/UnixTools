{
    TFile* f = TFile::Open("store_root/workspace_extraStep_3rd_sysmaticErrFit_noKinematicCut.root");
    TDirectory* d = (TDirectory*) f->Get("fitRes");
    TIter next(d->GetListOfKeys());
    TKey* key;
    //vector< TString > names;
    //names.reserve(200);
    TCanvas* c = new TCanvas("c1", "", 1000,500);
    c->Divide(2,1);

    if ( true )
    {
        c->cd(1);
        TH1D* h1 = new TH1D("hPos", "LbTk sys fit", 50,2000,3000);
        double origValLo=0.;
        double origValHi=0.;

        next = d->GetListOfKeys();
        while( (key=(TKey*)next()) )
        {
            TClass* clsPtr = gROOT->GetClass(key->GetClassName());
            TString name = key->GetClassName();
            TString objName = key->GetName();
            RooFitResult* res = (RooFitResult*) d->Get(objName);
            RooRealVar* numLb = (RooRealVar*) res->floatParsFinal().find("numLb");

            if ( objName.Contains("Lb")   )
            {
                if ( objName.Contains("data") )
                {
                    origValLo=numLb->getVal()+numLb->getErrorLo();
                    origValHi=numLb->getVal()+numLb->getErrorHi();
                    continue;
                }
                h1->Fill(numLb->getVal());
            }
        }
        h1->Draw();
        c->Update();

        TLine* ll = new TLine(origValLo,c->GetUymin(),origValLo,c->GetUymax());
        ll->SetLineColor(43);
        ll->Draw("same");
        TLine* lr = new TLine(origValHi,c->GetUymin(),origValHi,c->GetUymax());
        lr->SetLineColor(2);
        lr->Draw("same");
        h1->Draw("same");
    }

    if (true)
    {
        c->cd(2);
        TH1D* h2 = new TH1D("hNeg", "lBTk sys fit", 50,2000,3000);
        double origValLo=0.;
        double origValHi=0.;

        next = d->GetListOfKeys();
        while( (key=(TKey*)next()) )
        {
            TClass* clsPtr = gROOT->GetClass(key->GetClassName());
            TString name = key->GetClassName();
            TString objName = key->GetName();
            RooFitResult* res = (RooFitResult*) d->Get(objName);
            RooRealVar* numLb = (RooRealVar*) res->floatParsFinal().find("numlB");

            if ( objName.Contains("lB")   )
            {
                if ( objName.Contains("data") )
                {
                    origValLo=numLb->getVal()+numLb->getErrorLo();
                    origValHi=numLb->getVal()+numLb->getErrorHi();
                    continue;
                }
                h2->Fill(numLb->getVal());
            }
        }
        h2->Draw();
        c->Update();

        TLine* ll = new TLine(origValLo,c->GetUymin(),origValLo,c->GetUymax());
        ll->SetLineColor(43);
        ll->Draw("same");
        TLine* lr = new TLine(origValHi,c->GetUymin(),origValHi,c->GetUymax());
        lr->SetLineColor(2);
        lr->Draw("same");
        //h2->Draw("same");
    }
}

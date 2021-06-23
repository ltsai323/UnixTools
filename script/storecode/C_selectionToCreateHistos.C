{
    TFile* _file0 = TFile::Open("result_flatNtuple.root");
    TNtupleD* nt    = (TNtupleD*) _file0->Get("2016Data");
    TNtupleD* bd    = (TNtupleD*) _file0->Get("BdToJpsiKstar892");
    TNtupleD* bdbar = (TNtupleD*) _file0->Get("AntiBdToJpsiKstar892");
    TNtupleD* lb    = (TNtupleD*) _file0->Get("LbTk");
    TNtupleD* lbbar = (TNtupleD*) _file0->Get("AntiLbTk");
    TNtupleD* bsF   = (TNtupleD*) _file0->Get("BsToJpsiF");
    TNtupleD* bsKK  = (TNtupleD*) _file0->Get("BsToJpsiKK");
    
    TFile* newFile = new TFile("a.root", "recreate");
    TH1D* hlb1    = new TH1D("lbtk_2016Data" , "lbtkMass distribution in data", 140, 5.2,8.0);
    TH1D* hlb2    = new TH1D("lbtk_Bd"       , "lbtkMass distribution in Bd", 140, 5.2,8.0);
    TH1D* hlb3    = new TH1D("lbtk_AntiBd"   , "lbtkMass distribution in AntiBd", 140, 5.2,8.0);
    TH1D* hlbBKG  = new TH1D("lbtkCombBKG"   , "lbtkMass distribution in BKG ", 190, 5.1,7.0);

    TH1D* hbd1    = new TH1D("bd_2016Data"   , "bdMass distribution in data"  , 500, 4.5,7.0);
    TH1D* hbd2    = new TH1D("bd_Bd"         , "bdMass distribution in Bd"    , 500, 4.5,7.0);
    TH1D* hbd3    = new TH1D("bd_AntiBd"     , "bdMass distribution in AntiBd", 500, 4.5,7.0);

    TH1D* hbdbar1 = new TH1D("bdbar_2016Data", "bdbarMass distribution in data"  , 500, 4.5,7.0);
    TH1D* hbdbar2 = new TH1D("bdbar_Bd"      , "bdbarMass distribution in Bd"    , 500, 4.5,7.0);
    TH1D* hbdbar3 = new TH1D("bdbar_AntiBd"  , "bdbarMass distribution in AntiBd", 500, 4.5,7.0);

    TH1D* hbs1    = new TH1D("bs_2016Data"   , "bsMass distribution in data"  , 500, 4.5,7.0);
    TH1D* hbs2    = new TH1D("bs_Bd"         , "bsMass distribution in Bd"    , 500, 4.5,7.0);
    TH1D* hbs3    = new TH1D("bs_AntiBd"     , "bsMass distribution in AntiBd", 500, 4.5,7.0);


    nt   ->Draw("lbtkMass>>lbtk_2016Data" ,"lbtkMass>5.2&&lbtkMass<8.0");
    bd   ->Draw("lbtkMass>>lbtk_Bd"       ,"lbtkMass>5.2&&lbtkMass<8.0");
    bdbar->Draw("lbtkMass>>lbtk_AntiBd"   ,"lbtkMass>5.2&&lbtkMass<8.0");
                    
    nt   ->Draw("bdMass>>bd_2016Data"   ,"bdMass>4.5&&bdMass<7.0&&lbtkMass>5.2&&lbtkMass<8.0");
    bd   ->Draw("bdMass>>bd_Bd"         ,"bdMass>4.5&&bdMass<7.0&&lbtkMass>5.2&&lbtkMass<8.0");
    bdbar->Draw("bdMass>>bd_AntiBd"     ,"bdMass>4.5&&bdMass<7.0&&lbtkMass>5.2&&lbtkMass<8.0");
                    
    nt   ->Draw("bdbarMass>>bdbar_2016Data","bdbarMass>4.5&&bdbarMass<7.0&&lbtkMass>5.2&&lbtkMass<8.0");
    bd   ->Draw("bdbarMass>>bdbar_Bd"      ,"bdbarMass>4.5&&bdbarMass<7.0&&lbtkMass>5.2&&lbtkMass<8.0");
    bdbar->Draw("bdbarMass>>bdbar_AntiBd"  ,"bdbarMass>4.5&&bdbarMass<7.0&&lbtkMass>5.2&&lbtkMass<8.0");
                    
    nt   ->Draw("bsMass>>bs_2016Data"   ,"bsMass>4.5&&bsMass<7.0&&lbtkMass>5.2&&lbtkMass<10.0");
    bd   ->Draw("bsMass>>bs_Bd"         ,"bsMass>4.5&&bsMass<7.0&&lbtkMass>5.2&&lbtkMass<10.0");
    bdbar->Draw("bsMass>>bs_AntiBd"     ,"bsMass>4.5&&bsMass<7.0&&lbtkMass>5.2&&lbtkMass<10.0");
    nt   ->Draw("lbtkMass>>lbtkCombBKG","lbtkMass>5.1&&lbtkMass<7.0&&!(bdbarMass>5.22&&bdbarMass<5.33) &&!(bdMass>5.22&&bdMass<5.33) &&!(bsMass>5.32&&bsMass<5.40)");


    hlb1   ->Write();
    hlb2   ->Write();
    hlb3   ->Write();
    hlbBKG ->Write();
    hbd1   ->Write();
    hbd2   ->Write();
    hbd3   ->Write();
    hbdbar1->Write();
    hbdbar2->Write();
    hbdbar3->Write();
    hbs1   ->Write();
    hbs2   ->Write();
    hbs3   ->Write();

    lb->CloneTree(-1)->Write();
    lbbar->CloneTree(-1)->Write();
    bsF->CloneTree(-1)->Write();
    bsKK->CloneTree(-1)->Write();

    newFile->Close();
}


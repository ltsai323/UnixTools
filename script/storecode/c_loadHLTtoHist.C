{
    TFile* fin = TFile::Open("test.root");
    TTree* tree = (TTree*) fin->Get("treeCreatingSpecificDecay/pLbTk");

    int trigPass = 0;
    tree->SetBranchAddress("totallyTriggered", &trigPass);

    TH1I* h = new TH1I("hltRec", "HLT record status", 20, 0, 20 );

    unsigned idx = 0;
    unsigned ndx = tree->GetEntries();
    int HLT_target = 0;
    bool targetHLT = false;
    while( idx != ndx )
    {
        tree->GetEntry(idx++);
        for ( int i = 0; i < 20; ++i )
        {
            bool status = (trigPass >> i) % 2;
            if ( status )
            {
                h->Fill(i);
                if ( i == HLT_target )
                { targetHLT = true; }
            }
        }
    }
    if ( targetHLT )
        printf ("there is target HLT recorded!\n");
    else
        printf ( "nothing found\n");
    TCanvas* c1 = new TCanvas("c1","c1",1600,1600);
    h->Draw();
    c1->SaveAs("storefig/h_hltStatus.pdf");
}

const bool useHLTpreselect = true;
const int HLTNumber = 7;

bool passHLT( int recIntBool, int hltnum )
{ return (recIntBool>>num)%2; }





void c_loadTree()
{
    TFile* fIn = TFile::Open("/home/ltsai/Data/CRABdata/CRABdata_2016RunBv2_190516ReRunForFinal_11_06_2019/tot.root");
    TTree* tree = (TTree*) fIn->Get("VertexCompCandAnalyzer/pLbTk");

    TCanvas* c1 = new TCanvas("c1", "c1", 1600, 1000);
    tree->Draw()



}

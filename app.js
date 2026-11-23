/* ==========================================================================
   Donor Class Tracker — Interactive Multi-Sector Engine
   Client-Side Campaign Finance Analytics & Choropleth Visualization
   ========================================================================== */

(() => {
  const BUNDLE = window.DONOR_BUNDLE;
  if (!BUNDLE) {
    console.error("DONOR_BUNDLE not found. Ensure data/donor-dataset.js is loaded.");
    return;
  }

  // Application State
  const state = {
    activeSector: "all",
    activeMetric: "total",      // "total" | "avg" | "pct" | "per_capita"
    selectedState: "all",
    filterChamber: "all",       // "all" | "Senate" | "House"
    filterParty: "all",         // "all" | "Democrat" | "Republican" | "Independent"
    filterStatus: "Incumbent",  // "Incumbent" | "all"
    searchQuery: "",
    inspectorTab: "all",        // "all" | "senate" | "house"
    inspectorSearch: "",
    sort: "sector-desc",
    zoom: { scale: 1, x: 0, y: 0 },
    isDragging: false,
    dragStart: { x: 0, y: 0 },
    isEmbedded: false,
    activeModalCandidate: null
  };

  // Notification Toast Helper
  const showToast = (message) => {
    let toast = document.getElementById("donor-copy-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "donor-copy-toast";
      toast.className = "donor-copy-toast";
      toast.setAttribute("role", "status");
      toast.setAttribute("aria-live", "polite");
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
      toast.classList.remove("show");
    }, 2800);
  };

  // Clipboard Copy Helper (with modern API and textarea fallback for iframes)
  const copyTextToClipboard = async (text, successMessage) => {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        showToast(successMessage);
        return true;
      }
    } catch (e) {}

    try {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.style.position = "fixed";
      textarea.style.left = "-9999px";
      textarea.style.top = "0";
      textarea.setAttribute("readonly", "");
      document.body.appendChild(textarea);
      textarea.select();
      const successful = document.execCommand("copy");
      document.body.removeChild(textarea);
      if (successful) {
        showToast(successMessage);
        return true;
      }
    } catch (err) {}

    showToast("Copy failed: please select and copy manually");
    return false;
  };

  // Monetization & Google AdSense SPA Dynamic Refresh Controller
  const AdController = (() => {
    let lastRefreshTime = 0;
    const COOLDOWN_MS = 30000; // Strictly enforce 30s policy cooldown per Google AdSense guidelines
    let isInitialized = false;

    const init = () => {
      if (isInitialized) return;
      isInitialized = true;
      try {
        if (window.adsbygoogle) {
          const adSlots = document.querySelectorAll("ins.adsbygoogle");
          adSlots.forEach(() => {
            try {
              (window.adsbygoogle = window.adsbygoogle || []).push({});
            } catch (e) {}
          });
          lastRefreshTime = Date.now();
        }
      } catch (e) {}
    };

    const trigger = (reason) => {
      const now = Date.now();
      // Enforce 30-second cooldown between refresh requests
      if (now - lastRefreshTime < COOLDOWN_MS) {
        return false;
      }
      lastRefreshTime = now;

      try {
        if (window.adsbygoogle && typeof window.adsbygoogle.push === "function") {
          const adSlots = document.querySelectorAll("ins.adsbygoogle");
          adSlots.forEach(slot => {
            if (slot.getAttribute("data-adsbygoogle-status") === "done") {
              try {
                (window.adsbygoogle = window.adsbygoogle || []).push({});
              } catch (e) {}
            }
          });
        }
      } catch (e) {}
      return true;
    };

    return {
      init,
      trigger
    };
  })();

  const SECTORS = BUNDLE.sectors;
  const ALL_CANDIDATES = BUNDLE.candidates;
  const STATE_NAMES = BUNDLE.stateNames;
  const STATE_POP = BUNDLE.statePop;
  const US_PATHS = BUNDLE.usPaths;
  const CENTROIDS = BUNDLE.stateCentroids;

  const SMALL_STATES = ["DC", "RI", "DE", "CT", "NJ", "MA", "MD", "NH", "VT"];
  const TERRITORIES = ["PR", "GU", "VI", "AS", "MP"];

  // World Monitor & FEC Global Intelligence Live Wire
  const initNewsTicker = () => {
    const track = document.getElementById("ticker-track");
    if (!track) return;

    const baseItems = [
      { tag: "WORLD MONITOR // IRAN & RED SEA", text: "CENTCOM maritime air defense intercepts anti-ship ballistic strikes; naval strike groups maintain continuous patrol across Bab el-Mandeb chokepoint" },
      { tag: "GLOBAL HOTSPOTS // MILITARY BASES", text: "Pentagon expands forward basing posture in INDOPACOM & Middle East; defense contractors accelerate munition replenishment contracts" },
      { tag: "STRATEGIC WATERWAYS // MARITIME", text: "Strait of Hormuz & Suez Canal commercial transit re-routing exceeds 65%; global shipping rates surge amid escort deployments" },
      { tag: "ECONOMIC & SANCTIONS // OFAC", text: "U.S. Treasury implements targeted secondary sanctions enforcing crude oil price caps and interdicting shadow fleet maritime networks" },
      { tag: "FEC BENCHMARK // DEFENSE PACS", text: "Top defense aerospace PACs disburse contributions strictly within statutory $10K cycle caps across House & Senate Armed Services committees" },
      { tag: "NUCLEAR INFRASTRUCTURE // MONITOR", text: "IAEA verification teams monitor enrichment facilities amid heightened security postures across international defense installations" },
      { tag: "INFRASTRUCTURE & OUTAGES // ALERT", text: "North American & European energy grids heighten cyber-defense protocols around pipeline arteries and military logistics nodes" },
      { tag: "BIG PHARMA // CONGRESSIONAL HELP", text: "Healthcare & pharmaceutical PACs report $42.1M across House Energy & Commerce and Senate HELP committee leadership" },
      { tag: "WALL STREET // FINANCIAL SERVICES", text: "Banking & private equity PACs maintain fully capped contributions across key House Financial Services and Senate Banking leaders" },
      { tag: "FOREIGN POLICY ADVOCACY // COMPLIANCE", text: "All tracked advocacy PACs are domestic U.S. entities; federal law (52 U.S.C. § 30121) strictly prohibits foreign national contributions" },
      { tag: "OUTSIDE SPENDING // SUPER PACS", text: "Independent expenditure Super PACs register $110M+ in non-coordinated broadcast and digital ad disbursements" }
    ];

    const renderItems = (items) => {
      // Duplicate items to ensure smooth continuous marquee loop
      const combined = [...items, ...items];
      track.innerHTML = combined.map(it => `
        <div class="ticker-item">
          <strong>${it.tag}:</strong>
          <span>${it.text}</span>
        </div>
      `).join("");
    };

    renderItems(baseItems);
  };

  // Helper: Format Currency
  // Helper: Format Currency (Suppressed during official OpenFEC bulk rebuild)
  const formatMoney = (n) => "Rebuilding...";
  const formatMoneyFull = (n) => "Rebuilding from FEC records";
  // Helper: Get candidate contribution in active sector
  const getCandidateSectorAmount = (c, sectorKey) => {
    if (!c) return 0;
    if (sectorKey === "all") return c.totalPacAmount || 0;
    return (c.sectorTotals && c.sectorTotals[sectorKey]) || 0;
  };

  // Compute Aggregations for Active Sector across all 50 States
  const computeStateAggregations = () => {
    const stateMap = {};

    Object.keys(STATE_NAMES).forEach(st => {
      stateMap[st] = {
        code: st,
        name: STATE_NAMES[st],
        totalAmount: 0,
        incumbents: 0,
        fundedCount: 0,
        pop: STATE_POP[st] || 1000000,
        candidates: []
      };
    });

    ALL_CANDIDATES.forEach(c => {
      const st = c.state;
      if (!stateMap[st]) return;
      
      // Filter by party if selected
      if (state.filterParty !== "all" && c.party !== state.filterParty) return;

      const amt = getCandidateSectorAmount(c, state.activeSector);
      
      if (c.status === "Incumbent") {
        stateMap[st].incumbents++;
        if (amt > 0) stateMap[st].fundedCount++;
      }

      stateMap[st].totalAmount += amt;
      stateMap[st].candidates.push(c);
    });

    // Compute derived metrics
    Object.values(stateMap).forEach(s => {
      s.avgPerRep = s.incumbents > 0 ? (s.totalAmount / s.incumbents) : 0;
      s.pctFunded = s.incumbents > 0 ? (s.fundedCount / s.incumbents) * 100 : 0;
      s.perCapita = (s.totalAmount / s.pop) * 100000;
    });

    // Compute Rankings
    const rankedList = Object.values(stateMap).filter(s => !TERRITORIES.includes(s.code));
    
    const rankBy = (key) => {
      const sorted = [...rankedList].sort((a, b) => b[key] - a[key]);
      sorted.forEach((item, index) => {
        item[`rank_${key}`] = index + 1;
      });
    };

    rankBy("totalAmount");
    rankBy("avgPerRep");
    rankBy("pctFunded");
    rankBy("perCapita");

    return stateMap;
  };

  // Sector Color Mapping
  const getSectorColor = (sectorId) => {
    if (sectorId === "all") return "#38bdf8";
    if (SECTORS[sectorId]) return SECTORS[sectorId].color;
    return "#38bdf8";
  };

  // Generate Choropleth Color for a State
  const getStateFill = (stateData, metricKey, activeSector) => {
    if (!stateData) return "#1e2536";
    
    let val = 0;
    if (metricKey === "total") val = stateData.totalAmount;
    else if (metricKey === "avg") val = stateData.avgPerRep;
    else if (metricKey === "pct") val = stateData.pctFunded;
    else if (metricKey === "per_capita") val = stateData.perCapita;

    if (val <= 0) return "#151924";

    // Interpolate brightness based on rank
    const rankKey = metricKey === "total" ? "rank_totalAmount" :
                    metricKey === "avg" ? "rank_avgPerRep" :
                    metricKey === "pct" ? "rank_pctFunded" : "rank_perCapita";
    
    const rank = stateData[rankKey] || 50;
    // Rank 1 = most intense (index 0), Rank 50 = subtle
    const intensity = Math.max(0.18, 1 - (rank - 1) / 50);

    const baseHex = getSectorColor(activeSector);
    // Convert hex to rgb
    const r = parseInt(baseHex.slice(1, 3), 16);
    const g = parseInt(baseHex.slice(3, 5), 16);
    const b = parseInt(baseHex.slice(5, 7), 16);

    return `rgba(${r}, ${g}, ${b}, ${intensity.toFixed(2)})`;
  };

  // Render SVG Map
  const renderMap = (stateAggs) => {
    const statesGroup = document.getElementById("states-group");
    const labelsGroup = document.getElementById("labels-group");
    if (!statesGroup || !labelsGroup) return;

    statesGroup.innerHTML = "";
    labelsGroup.innerHTML = "";

    Object.entries(US_PATHS).forEach(([code, pathData]) => {
      const stateData = stateAggs[code];
      const fill = getStateFill(stateData, state.activeMetric, state.activeSector);
      
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", pathData);
      path.setAttribute("id", `state-${code}`);
      path.setAttribute("class", `state-path ${state.selectedState === code ? "selected" : ""}`);
      path.setAttribute("fill", fill);
      path.setAttribute("data-state", code);

      // Tooltip title
      const amtStr = stateData ? formatMoneyFull(stateData.totalAmount) : "$0";
      const nameStr = STATE_NAMES[code] || code;
      path.innerHTML = `<title>${nameStr} (${code}): ${amtStr}</title>`;

      path.addEventListener("click", () => {
        selectState(code, true);
      });

      statesGroup.appendChild(path);

      // Add State Centroid Label (if not small east coast state)
      const centroid = CENTROIDS[code];
      if (centroid && !SMALL_STATES.includes(code) && code !== "DC") {
        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", centroid[0]);
        text.setAttribute("y", centroid[1] + 4);
        text.setAttribute("text-anchor", "middle");
        text.setAttribute("class", "state-label-text");
        text.textContent = code;
        labelsGroup.appendChild(text);
      }
    });
  };

  // Render Callout Chips
  const renderCalloutChips = (stateAggs) => {
    const container = document.getElementById("callout-pills-container");
    if (!container) return;

    container.innerHTML = "";
    const list = [...SMALL_STATES, ...TERRITORIES];

    list.forEach(code => {
      const stateData = stateAggs[code];
      const btn = document.createElement("button");
      btn.className = `chip-btn ${state.selectedState === code ? "selected" : ""}`;
      const amt = stateData ? formatMoney(stateData.totalAmount) : "$0";
      btn.innerHTML = `${code} <span style="font-size: 0.65rem; color: var(--text-muted);">${amt}</span>`;
      btn.addEventListener("click", () => selectState(code, true));
      container.appendChild(btn);
    });
  };

  // Render Top Scoreboard Stats
  const renderScoreboard = (stateAggs) => {
    let grandTotal = 0;
    let fundedIncumbents = 0;
    let totalIncumbents = 0;

    ALL_CANDIDATES.forEach(c => {
      if (c.status !== "Incumbent") return; // Active Sitting 118th/119th Congress only
      if (state.filterParty !== "all" && c.party !== state.filterParty) return;
      const amt = getCandidateSectorAmount(c, state.activeSector);
      grandTotal += amt;
      totalIncumbents++;
      if (amt > 0) fundedIncumbents++;
    });

    const secMeta = SECTORS[state.activeSector];
    document.getElementById("stat-sector-total").textContent = formatMoney(grandTotal);

    const partyScopeStr = state.filterParty === "all" ? "" : ` (${state.filterParty}s)`;
    document.getElementById("stat-sector-name").textContent = `${secMeta ? secMeta.name : "All 7 Major Donor Sectors"}${partyScopeStr}`;

    document.getElementById("stat-members-funded").textContent = `${fundedIncumbents} / ${totalIncumbents}`;
    const pct = totalIncumbents > 0 ? ((fundedIncumbents / totalIncumbents) * 100).toFixed(1) : 0;
    const scopeLabel = state.filterParty === "all" ? "Sitting Congress" : `${state.filterParty} Incumbents`;
    document.getElementById("stat-funded-pct").textContent = `${pct}% of ${scopeLabel}`;

    // Top State
    const rankedStates = Object.values(stateAggs).filter(s => !TERRITORIES.includes(s.code)).sort((a, b) => b.totalAmount - a.totalAmount);
    const topState = rankedStates[0];
    if (topState && topState.totalAmount > 0) {
      document.getElementById("stat-top-state").textContent = `${topState.name} (${topState.code})`;
      document.getElementById("stat-top-state-amount").textContent = `${formatMoneyFull(topState.totalAmount)} total`;
    } else {
      document.getElementById("stat-top-state").textContent = "None";
      document.getElementById("stat-top-state-amount").textContent = "$0 total";
    }

    // Top Individual Recipient
    const sortedCandidates = [...ALL_CANDIDATES]
      .filter(c => c.status === "Incumbent" && (state.filterParty === "all" || c.party === state.filterParty))
      .sort((a, b) => getCandidateSectorAmount(b, state.activeSector) - getCandidateSectorAmount(a, state.activeSector));
    
    const topCand = sortedCandidates[0];
    if (topCand && getCandidateSectorAmount(topCand, state.activeSector) > 0) {
      const amt = getCandidateSectorAmount(topCand, state.activeSector);
      document.getElementById("stat-top-member").textContent = `${topCand.displayName} (${topCand.party[0]}-${topCand.state})`;
      document.getElementById("stat-top-member-details").textContent = `${formatMoneyFull(amt)} in ${secMeta ? secMeta.name : "Total PACs"}`;
    } else {
      document.getElementById("stat-top-member").textContent = "None";
      document.getElementById("stat-top-member-details").textContent = "$0 total";
    }
  };

  // Render High-Density Analytics Dashboard (Below Map)
  const renderAnalyticsDashboard = (stateAggs) => {
    const secMeta = SECTORS[state.activeSector];
    const activeSecName = secMeta ? secMeta.name : "All Major PACs";
    
    const dashSecNameEl = document.getElementById("dashboard-sector-name");
    if (dashSecNameEl) dashSecNameEl.textContent = activeSecName;

    // 1. Top 5 Powerhouse States in Active Sector
    const topStatesGrid = document.getElementById("top-states-ranking-grid");
    if (topStatesGrid) {
      topStatesGrid.innerHTML = "";
      const ranked = Object.values(stateAggs)
        .filter(s => !TERRITORIES.includes(s.code) && s.totalAmount > 0)
        .sort((a, b) => b.totalAmount - a.totalAmount)
        .slice(0, 5);

      ranked.forEach((st, idx) => {
        const chip = document.createElement("div");
        chip.className = `top-state-chip ${state.selectedState === st.code ? "selected" : ""}`;
        chip.innerHTML = `
          <span class="top-state-rank">#${idx + 1}</span>
          <span class="top-state-code">${st.code}</span>
          <span class="top-state-val">${formatMoney(st.totalAmount)}</span>
        `;
        chip.addEventListener("click", () => selectState(st.code));
        topStatesGrid.appendChild(chip);
      });
    }

    // 2. 7-Sector Contribution Proportion Stacked Bar
    const multiBar = document.getElementById("sector-multi-distribution-bar");
    const legendMini = document.getElementById("sector-legend-mini");
    if (multiBar && legendMini) {
      multiBar.innerHTML = "";
      legendMini.innerHTML = "";

      const pool = ALL_CANDIDATES.filter(c => {
        if (state.filterParty !== "all" && c.party !== state.filterParty) return false;
        if (state.filterStatus === "Incumbent" && c.status !== "Incumbent") return false;
        if (state.selectedState !== "all" && c.state !== state.selectedState) return false;
        return true;
      });

      const sectorSums = {};
      let allSectorTotal = 0;
      Object.keys(SECTORS).forEach(k => {
        sectorSums[k] = pool.reduce((acc, c) => acc + ((c.sectorTotals && c.sectorTotals[k]) || 0), 0);
        allSectorTotal += sectorSums[k];
      });

      Object.entries(SECTORS).forEach(([secId, meta]) => {
        const sum = sectorSums[secId] || 0;
        const pct = allSectorTotal > 0 ? (sum / allSectorTotal) * 100 : 14.28;

        const seg = document.createElement("div");
        seg.className = "sector-multi-segment";
        seg.style.width = `${pct}%`;
        seg.style.backgroundColor = meta.color;
        seg.title = `${meta.name}: ${formatMoneyFull(sum)} (${pct.toFixed(1)}%)`;
        multiBar.appendChild(seg);

        const leg = document.createElement("div");
        leg.className = "sector-legend-item";
        leg.innerHTML = `
          <span class="sector-legend-dot" style="background-color: ${meta.color};"></span>
          <span>${meta.shortName || meta.name} <strong>${pct.toFixed(0)}%</strong></span>
        `;
        legendMini.appendChild(leg);
      });
    }

    // 3. Chamber & Party Split Gauges
    const pool = ALL_CANDIDATES.filter(c => {
      if (state.filterStatus === "Incumbent" && c.status !== "Incumbent") return false;
      if (state.selectedState !== "all" && c.state !== state.selectedState) return false;
      return true;
    });

    let senAmt = 0;
    let houAmt = 0;
    let demAmt = 0;
    let repAmt = 0;

    pool.forEach(c => {
      const amt = getCandidateSectorAmount(c, state.activeSector);
      if (c.chamber === "Senate") senAmt += amt;
      else if (c.chamber === "House") houAmt += amt;

      if (c.party === "Democrat") demAmt += amt;
      else if (c.party === "Republican") repAmt += amt;
    });

    const totChamber = senAmt + houAmt || 1;
    const senPct = Math.round((senAmt / totChamber) * 100);
    const houPct = 100 - senPct;

    const chamberText = document.getElementById("chamber-split-text");
    if (chamberText) chamberText.textContent = `Senate ${senPct}% • House ${houPct}%`;
    const senBar = document.getElementById("chamber-bar-senate");
    if (senBar) senBar.style.width = `${senPct}%`;
    const houBar = document.getElementById("chamber-bar-house");
    if (houBar) houBar.style.width = `${houPct}%`;

    const totParty = demAmt + repAmt || 1;
    const demPct = Math.round((demAmt / totParty) * 100);
    const repPct = 100 - demPct;

    const partyText = document.getElementById("party-split-text");
    if (partyText) partyText.textContent = `Dem ${demPct}% • Rep ${repPct}%`;
    const demBar = document.getElementById("party-bar-dem");
    if (demBar) demBar.style.width = `${demPct}%`;
    const repBar = document.getElementById("party-bar-rep");
    if (repBar) repBar.style.width = `${repPct}%`;
  };

  // Render Inspector Panel (Scrollable Congressional Feed & State Delegation)
  const renderInspector = (stateAggs) => {
    const titleEl = document.getElementById("inspector-title");
    const subtitleEl = document.getElementById("inspector-subtitle");
    const sectorAmountEl = document.getElementById("inspector-sector-amount");
    const fundedRatioEl = document.getElementById("inspector-funded-ratio");
    const senateListEl = document.getElementById("senate-delegation-list");
    const houseListEl = document.getElementById("house-delegation-list");
    const senateSec = document.getElementById("senate-section");
    const houseSec = document.getElementById("house-section");
    const viewAllBtn = document.getElementById("btn-view-all-states");

    senateListEl.innerHTML = "";
    houseListEl.innerHTML = "";

    const activeSectorKey = state.activeSector;
    const searchFilter = (state.inspectorSearch || "").trim().toLowerCase();

    // Determine candidate pool for inspector
    let pool = [];
    if (state.selectedState === "all") {
      pool = ALL_CANDIDATES.filter(c => {
        if (state.filterStatus === "Incumbent" && c.status !== "Incumbent") return false;
        if (state.filterParty !== "all" && c.party !== state.filterParty) return false;
        return true;
      });
    } else {
      const stData = stateAggs[state.selectedState];
      if (stData) {
        pool = stData.candidates.filter(c => {
          if (state.filterStatus === "Incumbent" && c.status !== "Incumbent") return false;
          if (state.filterParty !== "all" && c.party !== state.filterParty) return false;
          return true;
        });
      }
    }

    // Apply inline inspector search if any
    if (searchFilter) {
      pool = pool.filter(c => {
        const name = (c.displayName || c.name || "").toLowerCase();
        const st = (c.state || "").toLowerCase();
        const dist = `${c.state}-${c.district || ''}`.toLowerCase();
        const fec = (c.fecCandidateId || "").toLowerCase();
        return name.includes(searchFilter) || st.includes(searchFilter) || dist.includes(searchFilter) || fec.includes(searchFilter);
      });
    }

    const senators = pool.filter(c => c.chamber === "Senate")
      .sort((a, b) => getCandidateSectorAmount(b, activeSectorKey) - getCandidateSectorAmount(a, activeSectorKey));

    const house = pool.filter(c => c.chamber === "House")
      .sort((a, b) => getCandidateSectorAmount(b, activeSectorKey) - getCandidateSectorAmount(a, activeSectorKey));

    // Update Tab Counters
    const tabCountAll = document.getElementById("tab-count-all");
    if (tabCountAll) tabCountAll.textContent = pool.length;
    const tabCountSen = document.getElementById("tab-count-sen");
    if (tabCountSen) tabCountSen.textContent = senators.length;
    const tabCountHou = document.getElementById("tab-count-hou");
    if (tabCountHou) tabCountHou.textContent = house.length;

    // Gracefully handle chamber tab visibility:
    // If the currently active tab has 0 members but the other chamber has members, default to 'all'
    if (state.inspectorTab === "senate" && senators.length === 0 && house.length > 0) {
      state.inspectorTab = "all";
      document.querySelectorAll(".inspector-tab").forEach(t => {
        t.classList.toggle("active", t.getAttribute("data-tab") === "all");
      });
    } else if (state.inspectorTab === "house" && house.length === 0 && senators.length > 0) {
      state.inspectorTab = "all";
      document.querySelectorAll(".inspector-tab").forEach(t => {
        t.classList.toggle("active", t.getAttribute("data-tab") === "all");
      });
    }

    if (state.inspectorTab === "senate") {
      senateSec.style.display = "block";
      houseSec.style.display = "none";
    } else if (state.inspectorTab === "house") {
      senateSec.style.display = "none";
      houseSec.style.display = "block";
    } else {
      senateSec.style.display = "block";
      houseSec.style.display = "block";
    }

    if (state.selectedState === "all") {
      titleEl.textContent = "United States";
      const partySub = state.filterParty === "all" ? "National Congressional Overview" : `National ${state.filterParty} Delegation`;
      subtitleEl.innerHTML = `<span>50 States + 5 Territories</span> • <span>${partySub}</span>`;
      viewAllBtn.style.display = "none";

      let nationalTotal = 0;
      let nationalFunded = 0;
      let totalIncumbents = 0;

      ALL_CANDIDATES.forEach(c => {
        if (state.filterParty !== "all" && c.party !== state.filterParty) return;
        if (c.status === "Incumbent") {
          totalIncumbents++;
          const amt = getCandidateSectorAmount(c, activeSectorKey);
          nationalTotal += amt;
          if (amt > 0) nationalFunded++;
        }
      });

      sectorAmountEl.textContent = formatMoney(nationalTotal);
      fundedRatioEl.textContent = `${nationalFunded} / ${totalIncumbents}`;

      const partyPrefix = state.filterParty === "all" ? "" : `${state.filterParty} `;
      document.getElementById("delegation-list-title").textContent = `U.S. Senate ${partyPrefix}(${senators.length} Members)`;
      document.getElementById("house-list-title").textContent = `U.S. House ${partyPrefix}(${house.length} Members)`;

      // Render senators (all matching in national view, scrollable!)
      senators.forEach(s => senateListEl.appendChild(createMemberRow(s, activeSectorKey)));
      if (senators.length === 0) {
        senateListEl.innerHTML = `<div class="delegation-empty-box">No senators found matching the active filter.</div>`;
      }

      // Render house (all matching in national view, scrollable!)
      house.forEach(h => houseListEl.appendChild(createMemberRow(h, activeSectorKey)));
      if (house.length === 0) {
        houseListEl.innerHTML = `<div class="delegation-empty-box">No representatives found matching the active filter.</div>`;
      }

    } else {
      // Selected specific state
      const stData = stateAggs[state.selectedState];
      if (!stData) return;

      titleEl.textContent = stData.name;
      const rankNum = stData.rank_totalAmount || "—";
      const partySuffix = state.filterParty === "all" ? "" : ` (${state.filterParty}s)`;
      subtitleEl.innerHTML = `<span>#${rankNum} in Nation for ${SECTORS[activeSectorKey] ? SECTORS[activeSectorKey].name : "Total PACs"}${partySuffix}</span>`;
      viewAllBtn.style.display = "inline-flex";

      sectorAmountEl.textContent = formatMoneyFull(stData.totalAmount);
      fundedRatioEl.textContent = `${stData.fundedCount} / ${stData.incumbents} (${stData.incumbents > 0 ? stData.pctFunded.toFixed(0) : 0}%)`;

      const partyScope = state.filterParty === "all" ? "" : `${state.filterParty} `;
      document.getElementById("delegation-list-title").textContent = `${stData.name} ${partyScope}Senate Delegation (${senators.length})`;
      document.getElementById("house-list-title").textContent = `${stData.name} ${partyScope}House Delegation (${house.length} Districts)`;

      if (pool.length === 0) {
        senateListEl.innerHTML = `
          <div class="delegation-empty-box">
            <div style="font-weight: 700; color: var(--text-primary); margin-bottom: 0.35rem;">No sitting ${partyScope}members in Congress from ${stData.name}.</div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.65rem;">This state delegation currently has zero seats held by ${partyScope}members.</p>
            <button class="btn btn-secondary btn-sm" id="btn-show-all-state-members">Show All ${stData.name} Members</button>
          </div>
        `;
        document.getElementById("btn-show-all-state-members")?.addEventListener("click", () => {
          state.filterParty = "all";
          document.querySelectorAll(".party-btn").forEach(b => b.classList.toggle("active", b.getAttribute("data-party") === "all"));
          const partySelect = document.getElementById("filter-party");
          if (partySelect) partySelect.value = "all";
          updateUI();
        });
      } else {
        senators.forEach(s => senateListEl.appendChild(createMemberRow(s, activeSectorKey)));
        if (senators.length === 0) {
          senateListEl.innerHTML = `
            <div class="delegation-empty-box">
              <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">No sitting ${partyScope}senators from ${stData.name}.</div>
              ${house.length > 0 ? `<div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.5rem;">Showing all ${house.length} ${partyScope}House ${house.length === 1 ? 'member' : 'members'} below.</div><button class="btn btn-secondary btn-sm" id="btn-jump-to-house" style="font-size: 0.75rem; padding: 0.25rem 0.6rem;">Jump to House Roster (${house.length})</button>` : ''}
            </div>
          `;
          document.getElementById("btn-jump-to-house")?.addEventListener("click", () => {
            document.getElementById("house-section")?.scrollIntoView({ behavior: "smooth", block: "start" });
          });
        }

        house.forEach(h => houseListEl.appendChild(createMemberRow(h, activeSectorKey)));
        if (house.length === 0) {
          houseListEl.innerHTML = `
            <div class="delegation-empty-box">
              <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">No sitting ${partyScope}representatives from ${stData.name}.</div>
              ${senators.length > 0 ? `<div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.5rem;">Showing all ${senators.length} ${partyScope}Senate ${senators.length === 1 ? 'member' : 'members'} above.</div><button class="btn btn-secondary btn-sm" id="btn-jump-to-senate" style="font-size: 0.75rem; padding: 0.25rem 0.6rem;">Jump to Senate Roster (${senators.length})</button>` : ''}
            </div>
          `;
          document.getElementById("btn-jump-to-senate")?.addEventListener("click", () => {
            document.getElementById("senate-section")?.scrollIntoView({ behavior: "smooth", block: "start" });
          });
        }
      }
    }
  };

  // Helper to create member inspector row
  const createMemberRow = (candidate, activeSectorKey) => {
    const row = document.createElement("div");
    row.className = "member-row";

    const partyClass = candidate.party === "Democrat" ? "badge-dem" :
                       candidate.party === "Republican" ? "badge-rep" : "badge-ind";

    const partyLetter = candidate.party ? candidate.party[0] : "I";
    const officeStr = candidate.chamber === "Senate" ? "Senate" : `District ${candidate.district || "At-Large"}`;
    const sectorAmt = getCandidateSectorAmount(candidate, activeSectorKey);

    // Compute progress percentage
    const maxReference = candidate.chamber === "Senate" ? 250000 : 120000;
    const barPct = Math.min(100, Math.round((sectorAmt / maxReference) * 100));

    row.innerHTML = `
      <img class="member-avatar" src="${candidate.photoUrl || ''}" alt="${candidate.displayName}" loading="lazy" onerror="this.src='https://unitedstates.github.io/images/congress/450x550/${candidate.fecCandidateId || 'placeholder'}.jpg';">
      <div>
        <div class="member-name">${candidate.displayName}</div>
        <div class="member-details">
          <span class="badge-party ${partyClass}">${partyLetter}</span>
          <span>${candidate.state} • ${officeStr}</span>
        </div>
        <div class="sector-mini-bar">
          <div class="sector-mini-fill" style="width: ${barPct}%;"></div>
        </div>
      </div>
      <div class="member-financials">
        <div class="financial-amount">${formatMoney(sectorAmt)}</div>
        <div class="financial-sub">in ${activeSectorKey === "all" ? "Total PACs" : SECTORS[activeSectorKey].name}</div>
      </div>
    `;

    row.addEventListener("click", () => openCandidateModal(candidate));
    return row;
  };

  // Active Filter Chips Strip Helper for Directory
  const renderDirectoryActiveFilterChips = (resultCount) => {
    const container = document.getElementById("directory-active-filters");
    if (!container) return;

    const chips = [];

    if (state.selectedState !== "all") {
      const sName = STATE_NAMES[state.selectedState] || state.selectedState;
      chips.push({
        label: `State: ${sName}`,
        clear: () => { selectState("all"); }
      });
    }

    if (state.filterParty !== "all") {
      chips.push({
        label: `Party: ${state.filterParty}`,
        clear: () => {
          state.filterParty = "all";
          document.querySelectorAll(".party-btn").forEach(b => b.classList.toggle("active", b.getAttribute("data-party") === "all"));
          const pSel = document.getElementById("filter-party");
          if (pSel) pSel.value = "all";
          updateUI();
        }
      });
    }

    if (state.filterChamber !== "all") {
      chips.push({
        label: `Chamber: ${state.filterChamber}`,
        clear: () => {
          state.filterChamber = "all";
          const cSel = document.getElementById("filter-chamber");
          if (cSel) cSel.value = "all";
          state.inspectorTab = "all";
          document.querySelectorAll(".inspector-tab").forEach(t => t.classList.toggle("active", t.getAttribute("data-tab") === "all"));
          updateUI();
        }
      });
    }

    if (state.activeSector !== "all") {
      const secName = SECTORS[state.activeSector] ? SECTORS[state.activeSector].name : state.activeSector;
      chips.push({
        label: `PAC: ${secName}`,
        clear: () => {
          state.activeSector = "all";
          document.querySelectorAll(".sector-pill").forEach(p => p.classList.toggle("active", p.getAttribute("data-sector") === "all"));
          updateUI();
        }
      });
    }

    if (state.searchQuery) {
      chips.push({
        label: `Search: "${state.searchQuery}"`,
        clear: () => {
          state.searchQuery = "";
          const sInput = document.getElementById("search-input");
          if (sInput) sInput.value = "";
          renderDirectory();
        }
      });
    }

    if (chips.length === 0) {
      container.style.display = "none";
      container.innerHTML = "";
      return;
    }

    container.style.display = "flex";
    container.innerHTML = `
      <span style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-muted); margin-right: 0.25rem;">Active (${resultCount}):</span>
    `;

    chips.forEach(chip => {
      const chipEl = document.createElement("span");
      chipEl.className = "filter-chip";
      chipEl.innerHTML = `${chip.label} <button class="filter-chip-remove" aria-label="Remove filter">&times;</button>`;
      chipEl.querySelector(".filter-chip-remove").addEventListener("click", chip.clear);
      container.appendChild(chipEl);
    });

    const clearAllBtn = document.createElement("button");
    clearAllBtn.className = "filter-chip-clear-all";
    clearAllBtn.textContent = "Clear All";
    clearAllBtn.addEventListener("click", () => {
      state.selectedState = "all";
      state.filterParty = "all";
      state.filterChamber = "all";
      state.activeSector = "all";
      state.searchQuery = "";
      const sInput = document.getElementById("search-input");
      if (sInput) sInput.value = "";
      document.querySelectorAll(".party-btn").forEach(b => b.classList.toggle("active", b.getAttribute("data-party") === "all"));
      document.querySelectorAll(".sector-pill").forEach(p => p.classList.toggle("active", p.getAttribute("data-sector") === "all"));
      const pSel = document.getElementById("filter-party");
      if (pSel) pSel.value = "all";
      const cSel = document.getElementById("filter-chamber");
      if (cSel) cSel.value = "all";
      updateUI();
    });
    container.appendChild(clearAllBtn);
  };

  // Render Full Member Directory Grid
  const renderDirectory = () => {
    const grid = document.getElementById("directory-grid");
    if (!grid) return;

    grid.innerHTML = "";

    const q = state.searchQuery.trim().toLowerCase();
    const activeSectorKey = state.activeSector;

    let filtered = ALL_CANDIDATES.filter(c => {
      // State Filter (Sync with state.selectedState)
      if (state.selectedState !== "all" && c.state !== state.selectedState) return false;
      // Chamber
      if (state.filterChamber !== "all" && c.chamber !== state.filterChamber) return false;
      // Party
      if (state.filterParty !== "all" && c.party !== state.filterParty) return false;
      // Status
      if (state.filterStatus === "Incumbent" && c.status !== "Incumbent") return false;

      // Text search (name, state, district, FEC candidate ID)
      if (q) {
        const matchName = (c.name || "").toLowerCase().includes(q) || (c.displayName || "").toLowerCase().includes(q);
        const matchState = (c.state || "").toLowerCase() === q || (STATE_NAMES[c.state] || "").toLowerCase().includes(q);
        const matchDistrict = `${c.state}-${c.district}`.toLowerCase().includes(q);
        const matchFec = (c.fecCandidateId || "").toLowerCase().includes(q);
        if (!matchName && !matchState && !matchDistrict && !matchFec) return false;
      }

      return true;
    });

    // Render Active Filter Chips
    renderDirectoryActiveFilterChips(filtered.length);

    // Sorting
    filtered.sort((a, b) => {
      if (state.sort === "sector-desc") {
        return getCandidateSectorAmount(b, activeSectorKey) - getCandidateSectorAmount(a, activeSectorKey);
      }
      if (state.sort === "total-desc") {
        return (b.totalPacAmount || 0) - (a.totalPacAmount || 0);
      }
      if (state.sort === "name-asc") {
        return (a.displayName || "").localeCompare(b.displayName || "");
      }
      return 0;
    });

    if (filtered.length === 0) {
      const stateName = STATE_NAMES[state.selectedState] || state.selectedState;
      const partyStr = state.filterParty === "all" ? "" : `${state.filterParty} `;
      const chamberStr = state.filterChamber === "all" ? "members" : `${state.filterChamber} members`;
      grid.innerHTML = `
        <div style="grid-column: 1 / -1; padding: 2.5rem 1rem; text-align: center; background-color: var(--bg-surface-elevated); border: 1px dashed var(--border-subtle); border-radius: var(--radius-md);">
          <div style="font-family: var(--font-display); font-size: 1.15rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.4rem;">
            No ${partyStr}${chamberStr} found${state.selectedState !== "all" ? ` for ${stateName}` : ""}.
          </div>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.85rem;">
            Try clearing filters or switching party / chamber to view all available members.
          </p>
          <button class="btn btn-secondary btn-sm" id="btn-directory-reset-all">Reset All Directory Filters</button>
        </div>
      `;
      document.getElementById("btn-directory-reset-all")?.addEventListener("click", () => {
        state.selectedState = "all";
        state.filterParty = "all";
        state.filterChamber = "all";
        state.searchQuery = "";
        const searchInput = document.getElementById("search-input");
        if (searchInput) searchInput.value = "";
        updateUI();
      });
      return;
    }

    // Render cards (limit to first 120 for instant DOM responsiveness)
    const displayList = filtered.slice(0, 120);

    displayList.forEach((c, idx) => {
      // In-feed Native Sponsor Spotlight Card at position #8
      if (idx === 8) {
        const sponsorCard = document.createElement("div");
        sponsorCard.className = "candidate-card sponsor-feed-card";
        sponsorCard.innerHTML = `
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.65rem;">
              <span class="ad-badge-sponsor">Civic Spotlight</span>
              <span style="font-family: var(--font-mono); font-size: 0.65rem; color: var(--text-muted);">SPONSORED BRIEFING</span>
            </div>
            <div style="font-family: var(--font-display); font-size: 1.15rem; font-weight: 700; color: var(--text-primary); line-height: 1.25; margin-bottom: 0.5rem;">
              Support Nonpartisan Campaign Finance Transparency
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.45; margin-bottom: 0.75rem;">
              Connect your organization, civic research initiative, or policy brief with 500,000+ informed voters, journalists, and institutional analysts.
            </p>
          </div>
          <div style="margin-top: auto; padding-top: 0.75rem; border-top: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.72rem; color: var(--text-muted); font-family: var(--font-mono);">INQUIRE:</span>
            <a href="mailto:advertise@donorclass.info" class="ad-link-btn" style="font-size: 0.75rem;">advertise@donorclass.info</a>
          </div>
        `;
        grid.appendChild(sponsorCard);
      }

      const card = document.createElement("div");
      card.className = "candidate-card";

      const partyClass = c.party === "Democrat" ? "badge-dem" :
                         c.party === "Republican" ? "badge-rep" : "badge-ind";
      const partyLetter = c.party ? c.party[0] : "I";
      const officeStr = c.chamber === "Senate" ? "Senate" : `District ${c.district || "AL"}`;
      const sectorAmt = getCandidateSectorAmount(c, activeSectorKey);

      card.innerHTML = `
        <div>
          <div class="card-top">
            <img class="card-avatar" src="${c.photoUrl || ''}" alt="${c.displayName}" loading="lazy">
            <div class="card-info">
              <div class="card-name">${c.displayName}</div>
              <div class="card-subtitle">
                <span class="badge-party ${partyClass}">${partyLetter}</span>
                ${c.state} • ${officeStr}
              </div>
            </div>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 0.5rem;">
            <span style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--text-muted); text-transform: uppercase;">${activeSectorKey === "all" ? "Total PAC $" : SECTORS[activeSectorKey].name}</span>
            <span style="font-family: var(--font-display); font-size: 1.25rem; font-weight: 700; color: var(--accent-active);">${formatMoney(sectorAmt)}</span>
          </div>
        </div>

        <div class="sector-breakdown-mini">
          <div class="breakdown-row">
            <span style="color: var(--text-muted); display: inline-flex; align-items: center; gap: 0.35rem;"><span class="sector-dot" style="background-color: var(--color-defense); width: 6px; height: 6px;"></span> Defense</span>
            <span>${formatMoney(c.sectorTotals ? c.sectorTotals.defense : 0)}</span>
          </div>
          <div class="breakdown-row">
            <span style="color: var(--text-muted); display: inline-flex; align-items: center; gap: 0.35rem;"><span class="sector-dot" style="background-color: var(--color-pharma); width: 6px; height: 6px;"></span> Pharma</span>
            <span>${formatMoney(c.sectorTotals ? c.sectorTotals.pharma : 0)}</span>
          </div>
          <div class="breakdown-row">
            <span style="color: var(--text-muted); display: inline-flex; align-items: center; gap: 0.35rem;"><span class="sector-dot" style="background-color: var(--color-finance); width: 6px; height: 6px;"></span> Finance</span>
            <span>${formatMoney(c.sectorTotals ? c.sectorTotals.finance : 0)}</span>
          </div>
          <div class="breakdown-row">
            <span style="color: var(--text-muted); display: inline-flex; align-items: center; gap: 0.35rem;"><span class="sector-dot" style="background-color: var(--color-energy); width: 6px; height: 6px;"></span> Energy</span>
            <span>${formatMoney(c.sectorTotals ? c.sectorTotals.energy : 0)}</span>
          </div>
        </div>
      `;

      card.addEventListener("click", () => openCandidateModal(c));
      grid.appendChild(card);
    });
  };

  // Open Candidate Detail Modal (<dialog>)
  const openCandidateModal = (candidate) => {
    state.activeModalCandidate = candidate;
    const modal = document.getElementById("candidate-modal");
    if (!modal) return;

    document.getElementById("modal-name").textContent = candidate.displayName;
    document.getElementById("modal-avatar").src = candidate.photoUrl || "";
    document.getElementById("modal-office").textContent = `${candidate.state} • ${candidate.chamber} (District ${candidate.district || "AL"})`;
    document.getElementById("modal-fec-id").textContent = `FEC ID: ${candidate.fecCandidateId || "N/A"}`;

    const partyBadge = document.getElementById("modal-party-badge");
    partyBadge.textContent = candidate.party;
    partyBadge.className = `badge-party ${candidate.party === "Democrat" ? "badge-dem" : candidate.party === "Republican" ? "badge-rep" : "badge-ind"}`;

    let breakdownHtml = `Total Tracked: ${formatMoneyFull(candidate.totalPacAmount)}`;
    if (candidate.outsideSpendingAmount > 0 || candidate.conduitAmount > 0) {
      breakdownHtml += ` <span style="font-size: 0.75rem; font-weight: normal; color: var(--text-muted);">(Direct: ${formatMoney(candidate.directPacAmount)} • Super PAC Outside Ads: ${formatMoney(candidate.outsideSpendingAmount)} • Conduit Bundles: ${formatMoney(candidate.conduitAmount)})</span>`;
    }
    document.getElementById("modal-total-pac-header").innerHTML = breakdownHtml;

    // Render 7-Sector Bars (No Emojis, Clean Colored Pips)
    const barsContainer = document.getElementById("modal-sector-bars");
    barsContainer.innerHTML = "";

    const maxSectorVal = Math.max(...Object.values(candidate.sectorTotals || { a: 1 }));

    Object.entries(SECTORS).forEach(([secId, secMeta]) => {
      const amt = (candidate.sectorTotals && candidate.sectorTotals[secId]) || 0;
      const barPct = maxSectorVal > 0 ? Math.min(100, Math.round((amt / maxSectorVal) * 100)) : 0;

      const item = document.createElement("div");
      item.className = "sector-bar-item";
      item.innerHTML = `
        <div class="sector-bar-meta">
          <span style="display: inline-flex; align-items: center; gap: 0.45rem;"><span class="sector-dot" style="background-color: ${secMeta.color}; width: 8px; height: 8px;"></span> ${secMeta.name}</span>
          <span style="font-family: var(--font-mono);">${formatMoneyFull(amt)}</span>
        </div>
        <div class="sector-bar-track">
          <div class="sector-bar-progress" style="width: ${barPct}%; background-color: ${secMeta.color};"></div>
        </div>
      `;
      barsContainer.appendChild(item);
    });

    // Render Top PACs Table for Active Sector
    const targetSector = state.activeSector === "all" ? "defense" : state.activeSector;
    document.getElementById("modal-active-sector-name").textContent = SECTORS[targetSector].name;

    const tbody = document.getElementById("modal-top-pacs-tbody");
    tbody.innerHTML = "";

    const pacList = (candidate.sectorTopPacs && candidate.sectorTopPacs[targetSector]) || [];
    if (pacList.length === 0) {
      tbody.innerHTML = `<tr><td colspan="2" style="color: var(--text-muted); text-align: center;">No itemized committee PAC contributions recorded in this sector.</td></tr>`;
    } else {
      pacList.forEach(pac => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>
            <div style="font-weight: 600;">${pac.name}</div>
            ${pac.type ? `<div style="font-size: 0.72rem; color: var(--text-muted);">${pac.type}${pac.note ? ` — <em>${pac.note}</em>` : ""}</div>` : ""}
          </td>
          <td style="vertical-align: top; font-family: var(--font-mono); font-weight: 600;">${formatMoneyFull(pac.amount)}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    // Populate Embed Code & Reset Embed Panel
    const origin = window.location.origin && window.location.origin !== "null" ? window.location.origin : "https://donorclass.info";
    const candIdentifier = candidate.fecCandidateId || candidate.slug || candidate.id;
    const embedCode = `<iframe src="${origin}/?candidate=${encodeURIComponent(candIdentifier)}&embed=true" width="100%" height="520" frameborder="0" loading="lazy" style="border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; max-width: 680px; width: 100%;"></iframe>`;
    const embedInput = document.getElementById("embed-code-input");
    if (embedInput) embedInput.value = embedCode;

    const embedPanel = document.getElementById("modal-embed-panel");
    if (embedPanel) embedPanel.style.display = "none";

    if (state.isEmbedded) {
      if (!modal.hasAttribute("open")) modal.setAttribute("open", "");
    } else {
      if (!modal.open) {
        try {
          modal.showModal();
        } catch (e) {
          modal.setAttribute("open", "");
        }
      }
    }
  };

  // State Selection Handler
  const selectState = (stateCode, isMapToggle = false) => {
    const prevState = state.selectedState;
    if (isMapToggle) {
      state.selectedState = state.selectedState === stateCode ? "all" : stateCode;
    } else {
      state.selectedState = (!stateCode || stateCode === "all") ? "all" : stateCode;
    }
    updateUI();

    // Throttled AdSense Dynamic Refresh (strictly respects 30s cooldown per Google AdSense SPA policy)
    if (state.selectedState !== prevState) {
      AdController.trigger("state_change");
    }

    // On mobile screens, smoothly scroll to the delegation inspector
    if (window.innerWidth < 768 && state.selectedState !== "all") {
      document.getElementById("inspector-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  // Update UI and Recolor
  const updateUI = () => {
    // Update active sector CSS variable for global accent glow
    const sectorColor = getSectorColor(state.activeSector);
    document.documentElement.style.setProperty("--accent-active", sectorColor);

    // Keep mobile state picker and directory state dropdown synced with current selection
    const mobileSel = document.getElementById("mobile-state-select");
    if (mobileSel && mobileSel.value !== state.selectedState) {
      mobileSel.value = state.selectedState;
    }
    const dirStateSel = document.getElementById("filter-state");
    if (dirStateSel && dirStateSel.value !== state.selectedState) {
      dirStateSel.value = state.selectedState;
    }

    const stateAggs = computeStateAggregations();
    renderScoreboard(stateAggs);
    renderMap(stateAggs);
    renderCalloutChips(stateAggs);
    renderAnalyticsDashboard(stateAggs);
    renderInspector(stateAggs);
    renderDirectory();
  };

  // CSV Export Handler
  const exportCSV = () => {
    const headers = ["Name", "Party", "State", "District", "Chamber", "Status", "Total_PAC_Money", "Direct_PAC_Capped", "Outside_SuperPAC_Spending", "Conduit_Earmarks", "Defense_PAC", "Pharma_PAC", "Finance_PAC", "Energy_PAC", "Tech_PAC", "ForeignPolicy_PAC", "Labor_PAC", "FEC_ID"];
    const rows = [headers.join(",")];

    ALL_CANDIDATES.forEach(c => {
      const st = c.sectorTotals || {};
      const row = [
        `"${c.displayName || c.name || ''}"`,
        `"${c.party || ''}"`,
        `"${c.state || ''}"`,
        `"${c.district || ''}"`,
        `"${c.chamber || ''}"`,
        `"${c.status || ''}"`,
        c.totalPacAmount || 0,
        c.directPacAmount || 0,
        c.outsideSpendingAmount || 0,
        c.conduitAmount || 0,
        st.defense || 0,
        st.pharma || 0,
        st.finance || 0,
        st.energy || 0,
        st.tech || 0,
        st.foreign_policy || 0,
        st.labor || 0,
        `"${c.fecCandidateId || ''}"`
      ];
      rows.push(row.join(","));
    });

    const blob = new Blob([rows.join("\n")], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `donor_class_congressional_pacs_${state.activeSector}_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Theme Management (Dark Mode vs Slate Grey) — Subdued Minimalist SVG Icons
  const applyTheme = (themeName) => {
    document.documentElement.setAttribute("data-theme", themeName);
    try {
      localStorage.setItem("donor_theme", themeName);
    } catch (e) {}

    const btn = document.getElementById("btn-theme-toggle");
    const svgEl = document.getElementById("theme-toggle-svg");
    if (svgEl) {
      if (themeName === "slate") {
        // Slate Grey / Background Lighting active: Clean Half-Sun on horizon with rays
        svgEl.innerHTML = `
          <path d="M2 18h20M6 18a6 6 0 0 1 12 0M12 4v4M4.93 7.93l2.83 2.83M19.07 7.93l-2.83 2.83" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/>
        `;
        if (btn) btn.setAttribute("title", "Theme: Slate Grey (Click for Dark Mode)");
      } else {
        // Dark Mode active: Clean Crescent Moon
        svgEl.innerHTML = `
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        `;
        if (btn) btn.setAttribute("title", "Theme: Dark Mode (Click for Slate Grey Theme)");
      }
    }
  };

  const toggleTheme = () => {
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    const next = current === "dark" ? "slate" : "dark";
    applyTheme(next);
  };

  // Setup Event Listeners
  const setupEventListeners = () => {
    // Theme Switcher Button
    const themeBtn = document.getElementById("btn-theme-toggle");
    if (themeBtn) themeBtn.addEventListener("click", toggleTheme);

    // Party Toggle Buttons (Map Controls)
    document.querySelectorAll(".party-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".party-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        state.filterParty = btn.getAttribute("data-party");

        // Sync with directory dropdown
        const partySelect = document.getElementById("filter-party");
        if (partySelect) partySelect.value = state.filterParty;

        const partyLabels = {
          all: "All Parties",
          Democrat: "Democrats Only",
          Republican: "Republicans Only",
          Independent: "Independents Only"
        };
        const partyLabelEl = document.getElementById("active-party-label");
        if (partyLabelEl) partyLabelEl.textContent = `Filter: ${partyLabels[state.filterParty] || state.filterParty}`;

        updateUI();
      });
    });

    // Sector Pills
    document.querySelectorAll(".sector-pill").forEach(pill => {
      pill.addEventListener("click", () => {
        document.querySelectorAll(".sector-pill").forEach(p => p.classList.remove("active"));
        pill.classList.add("active");
        state.activeSector = pill.getAttribute("data-sector");
        updateUI();
      });
    });

    // Metric Buttons
    document.querySelectorAll(".metric-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".metric-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        state.activeMetric = btn.getAttribute("data-metric");
        
        const labels = {
          total: "Total Sector PAC Contributions",
          avg: "Average Sector $ per Sitting Representative",
          pct: "Percentage of State Delegation Taking Sector Money",
          per_capita: "Sector Contributions per 100,000 State Residents"
        };
        document.getElementById("active-lens-label").textContent = `Metric: ${labels[state.activeMetric]}`;
        updateUI();
      });
    });

    // View All States Button in Inspector
    document.getElementById("btn-view-all-states").addEventListener("click", () => {
      state.selectedState = "all";
      updateUI();
    });

    // Inspector Filter Tabs (All / Senate / House)
    document.querySelectorAll(".inspector-tab").forEach(tab => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".inspector-tab").forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        state.inspectorTab = tab.getAttribute("data-tab");
        // Sync directory chamber filter
        state.filterChamber = state.inspectorTab === "senate" ? "Senate" :
                              state.inspectorTab === "house" ? "House" : "all";
        const chamSel = document.getElementById("filter-chamber");
        if (chamSel) chamSel.value = state.filterChamber;
        updateUI();
      });
    });

    // Inspector Inline Search
    const inspSearch = document.getElementById("inspector-search");
    if (inspSearch) {
      inspSearch.addEventListener("input", (e) => {
        state.inspectorSearch = e.target.value;
        const stateAggs = computeStateAggregations();
        renderInspector(stateAggs);
      });
    }

    // Search and Filters
    document.getElementById("search-input").addEventListener("input", (e) => {
      state.searchQuery = e.target.value;
      renderDirectory();
    });

    document.getElementById("filter-chamber").addEventListener("change", (e) => {
      state.filterChamber = e.target.value;
      const tabTarget = state.filterChamber === "all" ? "all" : state.filterChamber.toLowerCase();
      state.inspectorTab = tabTarget;
      document.querySelectorAll(".inspector-tab").forEach(t => {
        t.classList.toggle("active", t.getAttribute("data-tab") === tabTarget);
      });
      updateUI();
    });

    document.getElementById("filter-party").addEventListener("change", (e) => {
      state.filterParty = e.target.value;
      document.querySelectorAll(".party-btn").forEach(btn => {
        btn.classList.toggle("active", btn.getAttribute("data-party") === state.filterParty);
      });
      const partyLabels = {
        all: "All Parties",
        Democrat: "Democrats Only",
        Republican: "Republicans Only",
        Independent: "Independents Only"
      };
      const partyLabelEl = document.getElementById("active-party-label");
      if (partyLabelEl) partyLabelEl.textContent = `Filter: ${partyLabels[state.filterParty] || state.filterParty}`;
      updateUI();
    });

    document.getElementById("filter-status").addEventListener("change", (e) => {
      state.filterStatus = e.target.value;
      renderDirectory();
      const stateAggs = computeStateAggregations();
      renderInspector(stateAggs);
    });

    document.getElementById("filter-sort").addEventListener("change", (e) => {
      state.sort = e.target.value;
      renderDirectory();
    });

    // Modal close buttons
    const candModal = document.getElementById("candidate-modal");
    document.getElementById("btn-close-modal").addEventListener("click", () => candModal.close());
    candModal.addEventListener("click", (e) => {
      if (e.target === candModal && !state.isEmbedded) candModal.close();
    });

    // Embed & Share Actions in Candidate Modal
    const btnCopyLink = document.getElementById("btn-copy-dossier-link");
    if (btnCopyLink) {
      btnCopyLink.addEventListener("click", () => {
        if (!state.activeModalCandidate) return;
        const origin = window.location.origin && window.location.origin !== "null" ? window.location.origin : "https://donorclass.info";
        const candIdentifier = state.activeModalCandidate.fecCandidateId || state.activeModalCandidate.slug || state.activeModalCandidate.id;
        const shareUrl = `${origin}/?candidate=${encodeURIComponent(candIdentifier)}`;
        copyTextToClipboard(shareUrl, "Lawmaker dossier link copied to clipboard");
      });
    }

    const btnToggleEmbed = document.getElementById("btn-toggle-embed-code");
    const panelEmbed = document.getElementById("modal-embed-panel");
    if (btnToggleEmbed && panelEmbed) {
      btnToggleEmbed.addEventListener("click", () => {
        const isHidden = panelEmbed.style.display === "none" || !panelEmbed.style.display;
        panelEmbed.style.display = isHidden ? "flex" : "none";
        if (isHidden) {
          const input = document.getElementById("embed-code-input");
          if (input) input.select();
        }
      });
    }

    const btnCopyEmbed = document.getElementById("btn-copy-embed-code");
    if (btnCopyEmbed) {
      btnCopyEmbed.addEventListener("click", () => {
        const input = document.getElementById("embed-code-input");
        if (input && input.value) {
          copyTextToClipboard(input.value, "Embed HTML code copied to clipboard");
        }
      });
    }

    const methModal = document.getElementById("methodology-modal");
    document.getElementById("btn-methodology").addEventListener("click", () => methModal.showModal());
    document.getElementById("btn-close-methodology").addEventListener("click", () => methModal.close());
    methModal.addEventListener("click", (e) => {
      if (e.target === methModal) methModal.close();
    });

    // How to Use & FAQ Modal
    const walkModal = document.getElementById("walkthrough-modal");
    const btnWalk = document.getElementById("btn-walkthrough");
    const btnCloseWalk = document.getElementById("btn-close-walkthrough");
    const btnCloseExplore = document.getElementById("btn-close-and-explore");
    const tabBtnWalk = document.getElementById("tab-btn-walkthrough");
    const tabBtnFaq = document.getElementById("tab-btn-faq");
    const viewWalk = document.getElementById("view-walkthrough");
    const viewFaq = document.getElementById("view-faq");
    const faqSearchInput = document.getElementById("faq-search-input");

    if (walkModal) {
      if (btnWalk) btnWalk.addEventListener("click", () => walkModal.showModal());
      if (btnCloseWalk) btnCloseWalk.addEventListener("click", () => walkModal.close());
      if (btnCloseExplore) btnCloseExplore.addEventListener("click", () => walkModal.close());
      walkModal.addEventListener("click", (e) => {
        if (e.target === walkModal) walkModal.close();
      });

      // Tab toggling
      if (tabBtnWalk && tabBtnFaq) {
        tabBtnWalk.addEventListener("click", () => {
          tabBtnWalk.classList.add("active");
          tabBtnFaq.classList.remove("active");
          if (viewWalk) viewWalk.style.display = "block";
          if (viewFaq) viewFaq.style.display = "none";
        });
        tabBtnFaq.addEventListener("click", () => {
          tabBtnFaq.classList.add("active");
          tabBtnWalk.classList.remove("active");
          if (viewWalk) viewWalk.style.display = "none";
          if (viewFaq) viewFaq.style.display = "block";
        });
      }

      // Real-time FAQ search filter
      if (faqSearchInput) {
        faqSearchInput.addEventListener("input", (e) => {
          const q = (e.target.value || "").toLowerCase().trim();
          const items = document.querySelectorAll("#faq-accordion-list .faq-item");
          items.forEach(it => {
            const txt = (it.innerText || "").toLowerCase();
            if (!q || txt.includes(q)) {
              it.style.display = "";
              if (q) it.open = true;
            } else {
              it.style.display = "none";
            }
          });
        });
      }
    }

    // Collaborations & Suggestions Modal
    const contactModal = document.getElementById("contact-modal");
    const btnCollabHeader = document.getElementById("btn-collab-header");
    const btnCollabTrigger = document.getElementById("btn-collab-trigger");
    const btnCloseContact = document.getElementById("btn-close-contact");
    const contactForm = document.getElementById("contact-form");
    const contactStatusMsg = document.getElementById("contact-status-msg");
    const btnSubmitContact = document.getElementById("btn-submit-contact");
    const inputContactEmail = document.getElementById("contact-email");
    const inputContactMsg = document.getElementById("contact-msg");

    // Dynamic validation to enable Submit button only after user enters valid information
    const validateContactInputs = () => {
      const email = (inputContactEmail?.value || "").trim();
      const msg = (inputContactMsg?.value || "").trim();
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const isValid = emailRegex.test(email) && msg.length >= 5;

      if (btnSubmitContact) {
        btnSubmitContact.disabled = !isValid;
        btnSubmitContact.style.opacity = isValid ? "1" : "0.5";
        btnSubmitContact.style.cursor = isValid ? "pointer" : "not-allowed";
      }
    };

    if (inputContactEmail) inputContactEmail.addEventListener("input", validateContactInputs);
    if (inputContactMsg) inputContactMsg.addEventListener("input", validateContactInputs);

    // Ensure all dialogs start closed on load
    try {
      if (candModal && candModal.open) candModal.close();
      if (methModal && methModal.open) methModal.close();
      if (contactModal && contactModal.open) contactModal.close();
      if (walkModal && walkModal.open) walkModal.close();
    } catch (e) {}

    if (contactModal) {
      if (btnCollabHeader) {
        btnCollabHeader.addEventListener("click", () => {
          if (contactStatusMsg) contactStatusMsg.style.display = "none";
          contactModal.showModal();
          validateContactInputs();
        });
      }
      if (btnCollabTrigger) {
        btnCollabTrigger.addEventListener("click", () => {
          if (contactStatusMsg) contactStatusMsg.style.display = "none";
          contactModal.showModal();
          validateContactInputs();
        });
      }
      if (btnCloseContact) {
        btnCloseContact.addEventListener("click", () => contactModal.close());
      }
      contactModal.addEventListener("click", (e) => {
        if (e.target === contactModal) contactModal.close();
      });

      if (contactForm) {
        contactForm.addEventListener("submit", async (e) => {
          e.preventDefault();
          const topic = document.getElementById("contact-topic")?.value || "Collab / Suggestion";
          const name = document.getElementById("contact-name")?.value.trim() || "";
          const email = inputContactEmail?.value.trim() || "";
          const msg = inputContactMsg?.value.trim() || "";

          if (!email || !msg) return;

          if (btnSubmitContact) {
            btnSubmitContact.disabled = true;
            btnSubmitContact.style.opacity = "0.7";
            btnSubmitContact.style.cursor = "wait";
            btnSubmitContact.textContent = "Submitting...";
          }

          if (contactStatusMsg) {
            contactStatusMsg.style.display = "none";
          }

          const targetEmail = "contact@donorclass.info";
          const subject = `[DONOR CLASS] ${topic}${name ? ' - ' + name : ''}`;

          try {
            const response = await fetch(`https://formsubmit.co/ajax/${targetEmail}`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
              },
              body: JSON.stringify({
                name: name || "Anonymous Citizen",
                email: email,
                topic: topic,
                message: msg,
                _subject: subject,
                _template: "table",
                _captcha: "false"
              })
            });

            if (response.ok) {
              contactForm.reset();
              contactForm.style.display = "none";
              if (contactStatusMsg) {
                contactStatusMsg.style.display = "block";
                contactStatusMsg.innerHTML = `
                  <div style="padding: 1.5rem 0.5rem; text-align: center;">
                    <div style="font-family: var(--font-display); font-size: 1.35rem; font-weight: 700; color: var(--accent-active); margin-bottom: 0.5rem;">
                      Inquiry Received
                    </div>
                    <p style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.55; margin: 0 0 1.25rem 0;">
                      Your submission has been securely delivered to the Donor Class Research Desk. All feedback, data tips, and partnership proposals are reviewed confidentially.
                    </p>
                    <button type="button" class="btn btn-primary" id="btn-contact-done" style="margin: 0 auto; padding: 0.5rem 1.5rem;">
                      Done
                    </button>
                  </div>
                `;
                const btnDone = document.getElementById("btn-contact-done");
                if (btnDone) {
                  btnDone.addEventListener("click", () => {
                    contactModal.close();
                    contactForm.style.display = "block";
                    contactStatusMsg.style.display = "none";
                    validateContactInputs();
                  });
                }
              }
            } else {
              throw new Error("Submission returned non-200");
            }
          } catch (err) {
            // Graceful fallback: direct mail link to contact@donorclass.info
            if (btnSubmitContact) {
              btnSubmitContact.disabled = false;
              btnSubmitContact.style.opacity = "1";
              btnSubmitContact.style.cursor = "pointer";
              btnSubmitContact.textContent = "Submit";
            }
            if (contactStatusMsg) {
              contactStatusMsg.style.display = "block";
              contactStatusMsg.innerHTML = `
                <div style="color: #ef4444; font-size: 0.85rem; margin-top: 0.5rem;">
                  Direct network submission could not complete. You may reach out directly via:
                </div>
                <div style="margin-top: 0.65rem;">
                  <a href="mailto:${targetEmail}" class="btn btn-primary" style="display: inline-flex;">
                    ${targetEmail}
                  </a>
                </div>
              `;
            }
          }
        });
      }
    }

    // Export CSV
    document.getElementById("btn-export-csv").addEventListener("click", exportCSV);

    // Zoom and Pan Controls
    const transformGroup = document.getElementById("map-transform-group");
    const svgMap = document.getElementById("us-map-svg");

    const updateTransform = () => {
      transformGroup.setAttribute("transform", `translate(${state.zoom.x}, ${state.zoom.y}) scale(${state.zoom.scale})`);
    };

    document.getElementById("btn-zoom-in").addEventListener("click", () => {
      state.zoom.scale = Math.min(4.0, state.zoom.scale * 1.3);
      updateTransform();
    });

    document.getElementById("btn-zoom-out").addEventListener("click", () => {
      state.zoom.scale = Math.max(0.8, state.zoom.scale / 1.3);
      updateTransform();
    });

    document.getElementById("btn-zoom-reset").addEventListener("click", () => {
      state.zoom = { scale: 1, x: 0, y: 0 };
      state.selectedState = "all";
      updateTransform();
      updateUI();
    });

    // SVG Drag-to-Pan
    svgMap.addEventListener("mousedown", (e) => {
      if (e.target.tagName.toLowerCase() === "path") return; // Allow state clicks
      state.isDragging = true;
      state.dragStart = { x: e.clientX - state.zoom.x, y: e.clientY - state.zoom.y };
    });

    window.addEventListener("mousemove", (e) => {
      if (!state.isDragging) return;
      state.zoom.x = e.clientX - state.dragStart.x;
      state.zoom.y = e.clientY - state.dragStart.y;
      updateTransform();
    });

    window.addEventListener("mouseup", () => {
      state.isDragging = false;
    });
  };

  // State Selectors Setup (Mobile Jump Selector + Directory State Selector)
  const initStatePickers = () => {
    const pickers = [
      document.getElementById("mobile-state-select"),
      document.getElementById("filter-state")
    ].filter(Boolean);

    if (!STATE_NAMES || pickers.length === 0) return;

    const sorted = Object.entries(STATE_NAMES).sort((a, b) => a[1].localeCompare(b[1]));

    pickers.forEach(sel => {
      sel.innerHTML = '<option value="all">-- All 50 States (National Overview) --</option>';
      sorted.forEach(([code, name]) => {
        const opt = document.createElement("option");
        opt.value = code;
        opt.textContent = `${name} (${code})`;
        sel.appendChild(opt);
      });

      sel.addEventListener("change", (e) => {
        selectState(e.target.value);
      });
    });
  };

  // Candidate Resolver Helper (Supports FEC ID, slug, full name, or surname)
  const findCandidateByQuery = (query) => {
    if (!query || typeof query !== "string") return null;
    const raw = query.toLowerCase().trim();
    if (!raw) return null;

    const normalized = raw.replace(/[-_+]/g, " ").replace(/\s+/g, " ").trim();
    const slugified = normalized.replace(/\s+/g, "-");

    // 1. Exact match on FEC ID, slug, ID, or full name
    for (let i = 0; i < ALL_CANDIDATES.length; i++) {
      const c = ALL_CANDIDATES[i];
      const fec = (c.fecCandidateId || "").toLowerCase();
      const slug = (c.slug || "").toLowerCase();
      const id = (c.id || "").toLowerCase();
      const name = (c.displayName || c.name || "").toLowerCase();
      if (fec === raw || slug === slugified || slug === raw || id === raw || name === normalized) {
        return c;
      }
    }

    // 2. Exact word match on surname / slug segment
    for (let i = 0; i < ALL_CANDIDATES.length; i++) {
      const c = ALL_CANDIDATES[i];
      const slugParts = (c.slug || "").toLowerCase().split("-");
      const nameParts = (c.displayName || c.name || "").toLowerCase().split(/\s+/);
      if (slugParts.includes(raw) || nameParts.includes(normalized)) {
        return c;
      }
    }

    // 3. Substring match on name or slug
    for (let i = 0; i < ALL_CANDIDATES.length; i++) {
      const c = ALL_CANDIDATES[i];
      const slug = (c.slug || "").toLowerCase();
      const name = (c.displayName || c.name || "").toLowerCase();
      if (name.includes(normalized) || slug.includes(slugified) || slug.includes(raw)) {
        return c;
      }
    }

    return null;
  };

  // Initialization
  let savedTheme = "dark";
  try {
    savedTheme = localStorage.getItem("donor_theme") || "dark";
  } catch (e) {}
  applyTheme(savedTheme);

  // Parse URL Parameters (Deep Linking for Social Media & Campaign Distribution)
  let initialCandidateToOpen = null;
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const hash = window.location.hash;

    // Check for Embedded Mode (?embed=true or #embed)
    if (urlParams.get("embed") === "true" || hash === "#embed") {
      state.isEmbedded = true;
      document.body.classList.add("is-embedded");
    }

    const stParam = urlParams.get("state");
    if (stParam && (STATE_NAMES[stParam.toUpperCase()] || stParam === "all")) {
      state.selectedState = stParam.toUpperCase();
    }
    const secParam = urlParams.get("sector");
    if (secParam && (SECTORS[secParam.toLowerCase()] || secParam === "all")) {
      state.activeSector = secParam.toLowerCase();
      document.querySelectorAll(".sector-pill").forEach(p => {
        p.classList.toggle("active", p.getAttribute("data-sector") === state.activeSector);
      });
    }
    const partyParam = urlParams.get("party");
    if (partyParam && ["Democrat", "Republican", "Independent", "all"].includes(partyParam)) {
      state.filterParty = partyParam;
      document.querySelectorAll(".party-btn").forEach(b => {
        b.classList.toggle("active", b.getAttribute("data-party") === state.filterParty);
      });
      const pSel = document.getElementById("filter-party");
      if (pSel) pSel.value = state.filterParty;
    }

    // Direct Lawmaker Dossier Deep-Linking (?candidate=... or ?member=... or ?rep=...)
    const candParam = urlParams.get("candidate") || urlParams.get("member") || urlParams.get("rep");
    if (candParam) {
      const matched = findCandidateByQuery(candParam);
      if (matched) {
        state.selectedState = matched.state;
        initialCandidateToOpen = matched;
      }
    }
  } catch (e) {}

  initNewsTicker();
  initStatePickers();
  setupEventListeners();
  updateUI();
  AdController.init();

  if (initialCandidateToOpen) {
    openCandidateModal(initialCandidateToOpen);
    setTimeout(() => {
      openCandidateModal(initialCandidateToOpen);
    }, 60);
  }

  // Handle browser back/forward or hash change while staying on page
  window.addEventListener("popstate", () => {
    try {
      const params = new URLSearchParams(window.location.search);
      const cand = params.get("candidate") || params.get("member") || params.get("rep");
      if (cand) {
        const found = findCandidateByQuery(cand);
        if (found) {
          state.selectedState = found.state;
          updateUI();
          openCandidateModal(found);
        }
      } else {
        const modal = document.getElementById("candidate-modal");
        if (modal && modal.open && !state.isEmbedded) modal.close();
      }
    } catch (e) {}
  });
})();

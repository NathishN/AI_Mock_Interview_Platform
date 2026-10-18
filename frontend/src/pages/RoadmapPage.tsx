import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Map,
  Sparkles,
  Clock,
  CheckCircle2,
  BookOpen,
  Mic,
  ArrowRight,
  Circle,
} from 'lucide-react';
import { roadmapApi, LearningRoadmap, Milestone } from '../api/roadmap';

export const RoadmapPage: React.FC = () => {
  const [roadmap, setRoadmap] = useState<LearningRoadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [completedTasks, setCompletedTasks] = useState<Record<string, boolean>>({});

  useEffect(() => {
    roadmapApi
      .getRoadmap()
      .then((data) => setRoadmap(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));

    // Load saved checkbox progress from localStorage
    const saved = localStorage.getItem('roadmap_tasks');
    if (saved) {
      try {
        setCompletedTasks(JSON.parse(saved));
      } catch (e) {
        console.error(e);
      }
    }
  }, []);

  const toggleTask = (taskKey: string) => {
    setCompletedTasks((prev) => {
      const updated = { ...prev, [taskKey]: !prev[taskKey] };
      localStorage.setItem('roadmap_tasks', JSON.stringify(updated));
      return updated;
    });
  };

  if (loading) {
    return (
      <div className="py-24 text-center text-xs text-slate-500">
        <div className="w-7 h-7 border-3 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
        Building Tailored 4-Week Placement Roadmap...
      </div>
    );
  }

  if (!roadmap) {
    return (
      <div className="py-20 text-center text-xs text-slate-500">
        Roadmap could not be loaded. Please ensure you are logged in.
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-6 space-y-8">
      {/* Header */}
      <div className="space-y-1.5">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400">
          <Map className="w-3.5 h-3.5" />
          Strategic Placement Preparation
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          4-Week Learning Roadmap: {roadmap.target_role}
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
          A structured, milestone-driven curriculum designed to clear technical screenings, coding tests, and HR rounds.
        </p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-5 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm text-xs">
        <div>
          <span className="text-slate-400 font-medium">Curriculum Length</span>
          <div className="text-lg font-bold text-slate-900 dark:text-white mt-0.5">
            {roadmap.total_weeks} Weeks
          </div>
        </div>
        <div>
          <span className="text-slate-400 font-medium">Target Role</span>
          <div className="text-lg font-bold text-brand-600 dark:text-brand-400 mt-0.5 truncate">
            {roadmap.target_role}
          </div>
        </div>
        <div>
          <span className="text-slate-400 font-medium">Target Recruiters</span>
          <div className="text-lg font-bold text-slate-900 dark:text-white mt-0.5 truncate">
            {roadmap.target_companies.join(', ')}
          </div>
        </div>
        <div>
          <span className="text-slate-400 font-medium">Status</span>
          <div className="text-lg font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">
            Active Progress
          </div>
        </div>
      </div>

      {/* Milestones Timeline */}
      <div className="space-y-6">
        {roadmap.milestones.map((milestone) => (
          <div
            key={milestone.week}
            className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4"
          >
            {/* Milestone Header */}
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-3">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-brand-600 text-white font-extrabold flex items-center justify-center text-xs shadow-md">
                  W{milestone.week}
                </div>
                <div>
                  <h3 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white">
                    Week {milestone.week}: {milestone.title}
                  </h3>
                  <span className="text-xs text-brand-600 dark:text-brand-400 font-semibold">
                    Focus: {milestone.focus}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-1.5 text-xs text-slate-400 font-medium">
                <Clock className="w-3.5 h-3.5" />
                {milestone.estimated_hours} Hours Target
              </div>
            </div>

            {/* Topics Checklist */}
            <div className="space-y-2">
              <h4 className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                Core Placement Topics
              </h4>
              <div className="grid sm:grid-cols-2 gap-2 text-xs">
                {milestone.topics.map((topic, i) => {
                  const key = `w${milestone.week}_topic_${i}`;
                  const isDone = !!completedTasks[key];
                  return (
                    <div
                      key={i}
                      onClick={() => toggleTask(key)}
                      className={`p-2.5 rounded-xl border cursor-pointer select-none transition-colors flex items-center gap-2.5 ${
                        isDone
                          ? 'border-emerald-200 bg-emerald-50/40 dark:border-emerald-900 dark:bg-emerald-950/20 text-emerald-800 dark:text-emerald-300 line-through'
                          : 'border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
                      }`}
                    >
                      {isDone ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                      ) : (
                        <Circle className="w-4 h-4 text-slate-300 dark:text-slate-600 shrink-0" />
                      )}
                      <span>{topic}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Practice Actions */}
            <div className="space-y-2 pt-2">
              <h4 className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                Hands-on Practice Goals
              </h4>
              <div className="space-y-2 text-xs">
                {milestone.practice_actions.map((act, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800 flex items-center justify-between gap-3"
                  >
                    <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300">
                      <Sparkles className="w-3.5 h-3.5 text-brand-500" />
                      <span>{act}</span>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <Link
                        to="/library"
                        className="px-2.5 py-1 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:bg-slate-50 text-[11px] font-semibold text-slate-700 dark:text-slate-300 transition-colors"
                      >
                        Library
                      </Link>
                      <Link
                        to="/interview/new"
                        className="px-2.5 py-1 rounded-lg bg-brand-600 hover:bg-brand-700 text-white text-[11px] font-semibold transition-colors flex items-center gap-1"
                      >
                        Mock Room
                        <ArrowRight className="w-3 h-3" />
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
